"""Booking domain service — state machine and business logic."""

from datetime import datetime, timezone, timedelta
from decimal import Decimal

from flask import current_app

from app.extensions import db
from app.repositories import booking_repo, room_repo, user_repo
from app.services import audit_service, notification_service
from app.utils.errors import (
    NotFoundError,
    PermissionDeniedError,
    ConflictError,
    InvalidStateTransitionError,
    RoomUnavailableError,
)
from app.utils.dates import validate_booking_dates

# ---------------------------------------------------------------------------
# State machine
# ---------------------------------------------------------------------------

_ALLOWED: dict[str, set[str]] = {
    'draft': {'pending_admin_approval'},
    'pending_admin_approval': {'awaiting_payment', 'rejected', 'expired'},
    'awaiting_payment': {'payment_pending', 'expired', 'cancelled'},
    'payment_pending': {'confirmed', 'awaiting_payment', 'cancelled', 'expired'},
    'confirmed': {'checked_in', 'cancelled'},
    'checked_in': {'checked_out'},
    'checked_out': {'completed'},
}

_TERMINAL_STATUSES = {'checked_in', 'checked_out', 'completed', 'cancelled', 'expired', 'rejected'}


def _assert_transition(current_status: str, target_status: str) -> None:
    """Raise InvalidStateTransitionError if the transition is not allowed."""
    if target_status not in _ALLOWED.get(current_status, set()):
        raise InvalidStateTransitionError(
            f"Cannot transition from '{current_status}' to '{target_status}'"
        )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def create_booking(
    user_id: int,
    hostel_id: int,
    room_id: int,
    check_in,
    check_out,
    guests_count: int,
):
    """Create a new booking and submit it for admin approval."""
    validate_booking_dates(check_in, check_out)

    try:
        room = room_repo.find_available_locked(room_id, check_in, check_out)
        if room is None:
            raise RoomUnavailableError('Room is not available for the requested dates')

        if room.hostel_id != hostel_id:
            raise ConflictError('Room does not belong to the specified hostel', status_code=400)

        overlapping = booking_repo.find_overlapping(room_id, check_in, check_out)
        if overlapping:
            raise ConflictError('Room already has an active booking for these dates')

        active_blocks = booking_repo.find_active_blocks(room_id, check_in, check_out)
        if active_blocks:
            raise ConflictError('Room is blocked for these dates')

        total_amount = Decimal(str(room.price_per_night)) * (check_out - check_in).days
        hold_ttl = current_app.config.get('HOLD_TTL_MINUTES', 30)
        hold_expires_at = datetime.now(timezone.utc) + timedelta(minutes=hold_ttl)

        booking = booking_repo.create(
            user_id=user_id,
            hostel_id=hostel_id,
            room_id=room_id,
            check_in=check_in,
            check_out=check_out,
            guests_count=guests_count,
            total_amount=total_amount,
            hold_expires_at=hold_expires_at,
            status='pending_admin_approval',
        )

        audit_service.record('booking', booking.id, 'create', actor_user_id=user_id)
        db.session.commit()

        user = user_repo.get_by_id(user_id)
        if user:
            notification_service.send_booking_submitted(user.email, booking.id)

        return booking

    except (RoomUnavailableError, ConflictError, InvalidStateTransitionError):
        db.session.rollback()
        raise
    except Exception:
        db.session.rollback()
        raise


def get_booking(booking_id: int, actor_user_id: int, actor_role: str):
    """Load a booking; enforce owner-or-admin access control."""
    booking = booking_repo.get_by_id(booking_id)
    if booking is None:
        raise NotFoundError('Booking not found')
    if booking.user_id != actor_user_id and actor_role != 'admin':
        raise PermissionDeniedError('Access denied')
    return booking


def list_my_bookings(user_id: int, status: str | None = None, page: int = 1, per_page: int = 20):
    """Return paginated bookings for the given user."""
    return booking_repo.list_by_user(user_id, status=status, page=page, per_page=per_page)


def cancel_booking(booking_id: int, actor_user_id: int, actor_role: str):
    """Cancel a booking. Owners and admins may cancel."""
    booking = booking_repo.get_by_id(booking_id)
    if booking is None:
        raise NotFoundError('Booking not found')
    if booking.user_id != actor_user_id and actor_role != 'admin':
        raise PermissionDeniedError('Access denied')

    if booking.status in _TERMINAL_STATUSES:
        raise InvalidStateTransitionError(
            f"Cannot cancel a booking in '{booking.status}' state"
        )

    _assert_transition(booking.status, 'cancelled')
    booking.status = 'cancelled'
    db.session.flush()
    audit_service.record('booking', booking.id, 'cancel', actor_user_id=actor_user_id)
    db.session.commit()

    user = user_repo.get_by_id(booking.user_id)
    if user:
        notification_service.send_booking_cancelled(user.email, booking.id)

    return booking


def admin_approve(booking_id: int, admin_user_id: int, notes: str | None = None):
    """Admin approves a booking; extends the payment hold window."""
    booking = booking_repo.get_by_id(booking_id)
    if booking is None:
        raise NotFoundError('Booking not found')

    _assert_transition(booking.status, 'awaiting_payment')

    hold_ttl = current_app.config.get('HOLD_TTL_MINUTES', 30)
    booking.hold_expires_at = datetime.now(timezone.utc) + timedelta(minutes=hold_ttl)
    booking.status = 'awaiting_payment'
    if notes is not None:
        booking.admin_notes = notes

    db.session.flush()
    audit_service.record('booking', booking.id, 'approve', actor_user_id=admin_user_id)
    db.session.commit()

    user = user_repo.get_by_id(booking.user_id)
    if user:
        notification_service.send_booking_approved(user.email, booking.id)

    return booking


def admin_reject(booking_id: int, admin_user_id: int, notes: str | None = None):
    """Admin rejects a booking."""
    booking = booking_repo.get_by_id(booking_id)
    if booking is None:
        raise NotFoundError('Booking not found')

    _assert_transition(booking.status, 'rejected')
    booking.status = 'rejected'
    if notes is not None:
        booking.admin_notes = notes

    db.session.flush()
    audit_service.record('booking', booking.id, 'reject', actor_user_id=admin_user_id)
    db.session.commit()

    user = user_repo.get_by_id(booking.user_id)
    if user:
        notification_service.send_booking_rejected(user.email, booking.id, notes)

    return booking


def admin_checkin(booking_id: int, admin_user_id: int):
    """Admin marks a booking as checked in."""
    booking = booking_repo.get_by_id(booking_id)
    if booking is None:
        raise NotFoundError('Booking not found')

    _assert_transition(booking.status, 'checked_in')
    booking.status = 'checked_in'
    db.session.flush()
    audit_service.record('booking', booking.id, 'checkin', actor_user_id=admin_user_id)
    db.session.commit()
    return booking


def admin_checkout(booking_id: int, admin_user_id: int):
    """Admin marks a booking as checked out."""
    booking = booking_repo.get_by_id(booking_id)
    if booking is None:
        raise NotFoundError('Booking not found')

    _assert_transition(booking.status, 'checked_out')
    booking.status = 'checked_out'
    db.session.flush()
    audit_service.record('booking', booking.id, 'checkout', actor_user_id=admin_user_id)
    db.session.commit()
    return booking


def admin_complete(booking_id: int, admin_user_id: int):
    """Admin marks a booking as completed."""
    booking = booking_repo.get_by_id(booking_id)
    if booking is None:
        raise NotFoundError('Booking not found')

    _assert_transition(booking.status, 'completed')
    booking.status = 'completed'
    db.session.flush()
    audit_service.record('booking', booking.id, 'complete', actor_user_id=admin_user_id)
    db.session.commit()
    return booking


# ---------------------------------------------------------------------------
# System / internal helpers (called by payment_service, background jobs)
# ---------------------------------------------------------------------------

def system_start_payment_pending(booking) -> None:
    """Transition booking to payment_pending. Caller is responsible for commit."""
    _assert_transition(booking.status, 'payment_pending')
    booking.status = 'payment_pending'
    db.session.flush()


def system_mark_confirmed(booking) -> None:
    """Transition booking to confirmed. Caller is responsible for commit."""
    _assert_transition(booking.status, 'confirmed')
    booking.status = 'confirmed'
    db.session.flush()


def system_revert_to_awaiting(booking) -> None:
    """Revert a payment_pending booking back to awaiting_payment. Caller commits."""
    if booking.status == 'payment_pending':
        booking.status = 'awaiting_payment'
        db.session.flush()


def system_expire_holds() -> int:
    """Bulk-expire all stale holds. Returns count of expired bookings."""
    count = booking_repo.expire_holds(datetime.now(timezone.utc))
    db.session.commit()
    return count
