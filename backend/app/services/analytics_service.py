from datetime import date, datetime, timezone
from decimal import Decimal
from sqlalchemy import select, func, and_
from app.extensions import db
from app.models.booking import Booking, BookingStatus
from app.models.payment import Payment, PaymentStatus

def summary(date_from: date | None = None, date_to: date | None = None, granularity: str = 'daily') -> dict:
    """Admin analytics summary."""
    from datetime import timedelta
    now = datetime.now(timezone.utc).date()
    date_from = date_from or (now - timedelta(days=30))
    date_to = date_to or now

    # Booking counts by status
    booking_counts = {}
    rows = db.session.execute(
        select(Booking.status, func.count(Booking.id))
        .where(func.date(Booking.created_at) >= date_from, func.date(Booking.created_at) <= date_to)
        .group_by(Booking.status)
    ).all()
    for status, count in rows:
        booking_counts[status] = count
    total_bookings = sum(booking_counts.values())

    # Revenue (successful payments in range)
    revenue_row = db.session.execute(
        select(func.coalesce(func.sum(Payment.amount), 0))
        .where(
            Payment.status == PaymentStatus.SUCCESS.value,
            func.date(Payment.paid_at) >= date_from,
            func.date(Payment.paid_at) <= date_to,
        )
    ).scalar()
    revenue_total = Decimal(str(revenue_row))

    # Pending approvals
    pending_approvals = db.session.execute(
        select(func.count(Booking.id)).where(Booking.status == BookingStatus.PENDING_ADMIN_APPROVAL.value)
    ).scalar() or 0

    # Payment failures in range
    payment_failures = db.session.execute(
        select(func.count(Payment.id)).where(
            Payment.status == PaymentStatus.FAILED.value,
            func.date(Payment.created_at) >= date_from,
            func.date(Payment.created_at) <= date_to,
        )
    ).scalar() or 0

    # Revenue trend (bucketed by granularity)
    if granularity == 'monthly':
        bucket = func.date_trunc('month', Payment.paid_at)
    elif granularity == 'weekly':
        bucket = func.date_trunc('week', Payment.paid_at)
    else:
        bucket = func.date_trunc('day', Payment.paid_at)

    trend_rows = db.session.execute(
        select(bucket.label('period'), func.sum(Payment.amount).label('revenue'))
        .where(
            Payment.status == PaymentStatus.SUCCESS.value,
            func.date(Payment.paid_at) >= date_from,
            func.date(Payment.paid_at) <= date_to,
        )
        .group_by(bucket)
        .order_by(bucket)
    ).all()

    revenue_trend = [
        {'period': row.period.isoformat() if row.period else None, 'revenue': str(row.revenue or 0)}
        for row in trend_rows
    ]

    return {
        'bookings_total': total_bookings,
        'bookings_by_status': booking_counts,
        'revenue_total': str(revenue_total),
        'revenue_trend': revenue_trend,
        'pending_approvals': pending_approvals,
        'payment_failures': payment_failures,
        'date_from': str(date_from),
        'date_to': str(date_to),
        'granularity': granularity,
    }
