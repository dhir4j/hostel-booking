import enum
from datetime import datetime
from decimal import Decimal
from typing import Optional, TYPE_CHECKING
from sqlalchemy import BigInteger, String, Numeric, DateTime, Text, UniqueConstraint, Index, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db
from app.models._mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.booking import Booking

class PaymentStatus(str, enum.Enum):
    PENDING = 'pending'
    SUCCESS = 'success'
    FAILED = 'failed'
    REFUNDED = 'refunded'

class PaymentProviderEnum(str, enum.Enum):
    MOCK = 'mock'
    STRIPE = 'stripe'
    RAZORPAY = 'razorpay'

class Payment(TimestampMixin, db.Model):
    __tablename__ = 'payments'
    __table_args__ = (
        UniqueConstraint('provider', 'provider_ref', name='uq_payments_provider_ref'),
        CheckConstraint('amount >= 0', name='ck_payments_amount'),
        Index('ix_payments_booking_status', 'booking_id', 'status'),
        Index('ix_payments_status', 'status'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    booking_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('bookings.id', ondelete='CASCADE'), nullable=False)
    provider: Mapped[str] = mapped_column(String(30), nullable=False)
    provider_ref: Mapped[Optional[str]] = mapped_column(String(120))
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default='INR')
    status: Mapped[str] = mapped_column(String(20), nullable=False, default=PaymentStatus.PENDING.value)
    failure_reason: Mapped[Optional[str]] = mapped_column(Text)
    paid_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    booking: Mapped['Booking'] = relationship('Booking', back_populates='payments')
