from datetime import datetime

from sqlalchemy import select, func, update as sa_update

from app.extensions import db
from app.models.booking import Booking
from app.models.room import RoomBlock

_ACTIVE_STATUSES = (
    'pending_admin_approval',
    'awaiting_payment',
    'payment_pending',
    'confirmed',
    'checked_in',
)


def get_by_id(booking_id: int) -> Booking | None:
    return db.session.get(Booking, booking_id)


def create(
    user_id: int,
    hostel_id: int,
    room_id: int,
    check_in,
    check_out,
    guests_count: int,
    total_amount: float,
    hold_expires_at,
    status: str,
) -> Booking:
    booking = Booking(
        user_id=user_id,
        hostel_id=hostel_id,
        room_id=room_id,
        check_in=check_in,
        check_out=check_out,
        guests_count=guests_count,
        total_amount=total_amount,
        hold_expires_at=hold_expires_at,
        status=status,
    )
    db.session.add(booking)
    db.session.flush()
    return booking


def update(booking: Booking, **kwargs) -> Booking:
    for k, v in kwargs.items():
        setattr(booking, k, v)
    db.session.flush()
    return booking


def list_by_user(
    user_id: int,
    status: str | None = None,
    page: int = 1,
    per_page: int = 20,
) -> tuple[list, int]:
    stmt = select(Booking).where(Booking.user_id == user_id)
    if status:
        stmt = stmt.where(Booking.status == status)

    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = db.session.execute(count_stmt).scalar_one()

    stmt = stmt.offset((page - 1) * per_page).limit(per_page)
    rows = db.session.execute(stmt).scalars().all()
    return list(rows), total


def list_admin(
    status: str | None = None,
    hostel_id: int | None = None,
    user_id: int | None = None,
    date_from=None,
    date_to=None,
    page: int = 1,
    per_page: int = 20,
) -> tuple[list, int]:
    stmt = select(Booking)
    if status:
        stmt = stmt.where(Booking.status == status)
    if hostel_id is not None:
        stmt = stmt.where(Booking.hostel_id == hostel_id)
    if user_id is not None:
        stmt = stmt.where(Booking.user_id == user_id)
    if date_from is not None:
        stmt = stmt.where(Booking.check_in >= date_from)
    if date_to is not None:
        stmt = stmt.where(Booking.check_out <= date_to)

    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = db.session.execute(count_stmt).scalar_one()

    stmt = stmt.offset((page - 1) * per_page).limit(per_page)
    rows = db.session.execute(stmt).scalars().all()
    return list(rows), total


def find_overlapping(room_id: int, check_in, check_out, exclude_id: int | None = None) -> list[Booking]:
    stmt = select(Booking).where(
        Booking.room_id == room_id,
        Booking.check_in < check_out,
        Booking.check_out > check_in,
        Booking.status.in_(_ACTIVE_STATUSES),
    )
    if exclude_id is not None:
        stmt = stmt.where(Booking.id != exclude_id)
    return list(db.session.execute(stmt).scalars().all())


def find_active_blocks(room_id: int, check_in, check_out) -> list[RoomBlock]:
    stmt = select(RoomBlock).where(
        RoomBlock.room_id == room_id,
        RoomBlock.start_date < check_out,
        RoomBlock.end_date > check_in,
    )
    return list(db.session.execute(stmt).scalars().all())


def expire_holds(now: datetime) -> int:
    stmt = (
        sa_update(Booking)
        .where(
            Booking.hold_expires_at < now,
            Booking.status.in_(('pending_admin_approval', 'awaiting_payment', 'payment_pending')),
        )
        .values(status='expired')
        .execution_options(synchronize_session='fetch')
    )
    result = db.session.execute(stmt)
    db.session.flush()
    return result.rowcount
