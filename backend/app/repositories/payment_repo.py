from sqlalchemy import select, func

from app.extensions import db
from app.models.payment import Payment


def get_by_id(payment_id: int) -> Payment | None:
    return db.session.get(Payment, payment_id)


def get_by_provider_ref(provider: str, provider_ref: str) -> Payment | None:
    stmt = select(Payment).where(
        Payment.provider == provider,
        Payment.provider_ref == provider_ref,
    )
    return db.session.execute(stmt).scalar_one_or_none()


def create(
    booking_id: int,
    provider: str,
    amount: float,
    currency: str = 'INR',
    provider_ref: str | None = None,
) -> Payment:
    payment = Payment(
        booking_id=booking_id,
        provider=provider,
        amount=amount,
        currency=currency,
        provider_ref=provider_ref,
    )
    db.session.add(payment)
    db.session.flush()
    return payment


def update(payment: Payment, **kwargs) -> Payment:
    for k, v in kwargs.items():
        setattr(payment, k, v)
    db.session.flush()
    return payment


def list_by_booking(booking_id: int) -> list[Payment]:
    stmt = select(Payment).where(Payment.booking_id == booking_id)
    return list(db.session.execute(stmt).scalars().all())


def list_admin(
    status: str | None = None,
    date_from=None,
    date_to=None,
    page: int = 1,
    per_page: int = 20,
) -> tuple[list, int]:
    stmt = select(Payment)
    if status:
        stmt = stmt.where(Payment.status == status)
    if date_from is not None:
        stmt = stmt.where(Payment.created_at >= date_from)
    if date_to is not None:
        stmt = stmt.where(Payment.created_at <= date_to)

    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = db.session.execute(count_stmt).scalar_one()

    stmt = stmt.offset((page - 1) * per_page).limit(per_page)
    rows = db.session.execute(stmt).scalars().all()
    return list(rows), total


def get_latest_for_booking(booking_id: int) -> Payment | None:
    stmt = (
        select(Payment)
        .where(Payment.booking_id == booking_id)
        .order_by(Payment.created_at.desc())
        .limit(1)
    )
    return db.session.execute(stmt).scalar_one_or_none()
