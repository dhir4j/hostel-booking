"""Payment domain service — intent creation, webhook handling, reconciliation."""

from datetime import datetime, timezone
from decimal import Decimal

from app.extensions import db
from app.repositories import payment_repo, booking_repo
from app.services import booking_service, audit_service, notification_service
from app.payments.factory import get_provider
from app.utils.errors import (
    NotFoundError,
    PermissionDeniedError,
    BusinessRuleError,
    PaymentError,
)


def create_intent(booking_id: int, user_id: int) -> dict:
    """Create a payment intent for a booking in awaiting_payment state."""
    booking = booking_repo.get_by_id(booking_id)
    if not booking:
        raise NotFoundError('Booking not found')
    if booking.user_id != user_id:
        raise PermissionDeniedError('Not your booking')
    if booking.status != 'awaiting_payment':
        raise BusinessRuleError(
            f'Booking must be in awaiting_payment state, got {booking.status}'
        )

    provider = get_provider()
    amount = Decimal(str(booking.total_amount))
    result = provider.create_intent(
        booking=booking,
        amount=amount,
        currency='INR',
        metadata={'booking_id': booking_id, 'user_id': user_id},
    )

    payment = payment_repo.create(
        booking_id=booking_id,
        provider=provider.name,
        amount=amount,
        currency='INR',
        provider_ref=result.get('provider_ref'),
    )

    booking_service.system_start_payment_pending(booking)
    db.session.commit()

    return {
        'provider': provider.name,
        'provider_ref': result.get('provider_ref'),
        'client_secret': result.get('client_secret'),
        'amount': str(amount),
        'currency': 'INR',
        'payment_id': payment.id,
    }


def handle_webhook(provider_name: str, headers, raw_body: bytes) -> dict:
    """Verify and process an inbound payment provider webhook."""
    provider = get_provider(provider_name)
    try:
        event = provider.verify_webhook(headers=headers, raw_body=raw_body)
    except ValueError as e:
        raise PaymentError(str(e), code='INVALID_SIGNATURE', status_code=400)

    provider_ref = event['provider_ref']

    # Idempotency check — skip already-terminal payments.
    existing = payment_repo.get_by_provider_ref(provider_name, provider_ref)
    if existing and existing.status in ('success', 'failed', 'refunded'):
        return {'status': 'duplicate', 'payment_id': existing.id}

    status = event['status']  # 'success' or 'failed'

    if existing:
        payment_repo.update(
            existing,
            status='success' if status == 'success' else 'failed',
            paid_at=datetime.now(timezone.utc) if status == 'success' else None,
            failure_reason=event.get('failure_reason'),
        )
        payment = existing
    else:
        payment = payment_repo.create(
            booking_id=None,  # resolved via provider_ref lookup — skipped for now
            provider=provider_name,
            amount=Decimal(str(event.get('amount', 0))),
            currency=event.get('currency', 'INR'),
            provider_ref=provider_ref,
        )
        payment_repo.update(payment, status='success' if status == 'success' else 'failed')

    booking = booking_repo.get_by_id(payment.booking_id) if payment.booking_id else None
    if booking:
        if status == 'success':
            booking_service.system_mark_confirmed(booking)
            audit_service.record('payment', payment.id, 'webhook_success')
            db.session.commit()

            from app.repositories import user_repo
            user = user_repo.get_by_id(booking.user_id)
            if user:
                notification_service.send_payment_confirmed(user.email, booking.id)
        else:
            booking_service.system_revert_to_awaiting(booking)
            audit_service.record('payment', payment.id, 'webhook_failure')
            db.session.commit()
    else:
        db.session.commit()

    return {'status': 'processed', 'payment_id': payment.id}


def get_status(booking_id: int, actor_user_id: int, actor_role: str) -> dict:
    """Return booking and latest payment status for the given booking."""
    booking = booking_repo.get_by_id(booking_id)
    if not booking:
        raise NotFoundError('Booking not found')
    if booking.user_id != actor_user_id and actor_role != 'admin':
        raise PermissionDeniedError('Access denied')

    last_payment = payment_repo.get_latest_for_booking(booking_id)
    return {
        'booking_id': booking_id,
        'booking_status': booking.status,
        'payment_status': last_payment.status if last_payment else None,
        'last_payment': last_payment,
    }


def admin_reconcile(payment_id: int, actor_user_id: int) -> dict:
    """Fetch live status from the provider and sync it to the local payment record."""
    payment = payment_repo.get_by_id(payment_id)
    if not payment:
        raise NotFoundError('Payment not found')

    provider = get_provider(payment.provider)
    result = provider.fetch_payment_status(payment.provider_ref)
    new_status = result.get('status', payment.status)
    payment_repo.update(payment, status=new_status)
    audit_service.record('payment', payment_id, 'reconcile', actor_user_id=actor_user_id)
    db.session.commit()
    return payment


def admin_refund(payment_id: int, actor_user_id: int) -> dict:
    """Issue a full refund for a successful payment."""
    payment = payment_repo.get_by_id(payment_id)
    if not payment:
        raise NotFoundError('Payment not found')
    if payment.status != 'success':
        raise BusinessRuleError('Can only refund successful payments')

    provider = get_provider(payment.provider)
    provider.refund(payment.provider_ref, amount=Decimal(str(payment.amount)))
    payment_repo.update(payment, status='refunded')
    audit_service.record('payment', payment_id, 'refund', actor_user_id=actor_user_id)
    db.session.commit()
    return payment
