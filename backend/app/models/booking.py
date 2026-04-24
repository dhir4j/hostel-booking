import enum
from datetime import date, datetime
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import BigInteger, SmallInteger, Integer, Numeric, Date, DateTime, Text, String, CheckConstraint, Index, Computed, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db
from app.models._mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.hostel import Hostel
    from app.models.room import Room
    from app.models.payment import Payment

VALID_BOOKING_STATUSES = [
    'draft', 'pending_admin_approval', 'awaiting_payment', 'payment_pending',
    'confirmed', 'checked_in', 'checked_out', 'completed',
    'rejected', 'cancelled', 'expired'
]

class BookingStatus(str, enum.Enum):
    DRAFT = 'draft'
    PENDING_ADMIN_APPROVAL = 'pending_admin_approval'
    AWAITING_PAYMENT = 'awaiting_payment'
    PAYMENT_PENDING = 'payment_pending'
    CONFIRMED = 'confirmed'
    CHECKED_IN = 'checked_in'
    CHECKED_OUT = 'checked_out'
    COMPLETED = 'completed'
    REJECTED = 'rejected'
    CANCELLED = 'cancelled'
    EXPIRED = 'expired'

class Booking(TimestampMixin, db.Model):
    __tablename__ = 'bookings'
    __table_args__ = (
        CheckConstraint('check_out > check_in', name='ck_bookings_dates_order'),
        CheckConstraint('guests_count > 0', name='ck_bookings_guests'),
        CheckConstraint('total_amount >= 0', name='ck_bookings_amount'),
        CheckConstraint(
            "status IN ('draft','pending_admin_approval','awaiting_payment','payment_pending','confirmed','checked_in','checked_out','completed','rejected','cancelled','expired')",
            name='ck_bookings_status'
        ),
        Index('ix_bookings_room_dates', 'room_id', 'check_in', 'check_out'),
        Index('ix_bookings_user', 'user_id', 'created_at'),
        Index('ix_bookings_hostel_status', 'hostel_id', 'status'),
        Index('ix_bookings_status', 'status'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id', ondelete='RESTRICT'), nullable=False)
    hostel_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('hostels.id', ondelete='RESTRICT'), nullable=False)
    room_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('rooms.id', ondelete='RESTRICT'), nullable=False)
    check_in: Mapped[date] = mapped_column(Date, nullable=False)
    check_out: Mapped[date] = mapped_column(Date, nullable=False)
    guests_count: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    nights_count: Mapped[int] = mapped_column(Integer, Computed('check_out - check_in', persisted=True), nullable=False)
    total_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default=BookingStatus.PENDING_ADMIN_APPROVAL.value)
    admin_notes: Mapped[Optional[str]] = mapped_column(Text)
    hold_expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    user: Mapped['User'] = relationship('User', back_populates='bookings')
    hostel: Mapped['Hostel'] = relationship('Hostel', back_populates='bookings')
    room: Mapped['Room'] = relationship('Room', back_populates='bookings')
    payments: Mapped[List['Payment']] = relationship('Payment', back_populates='booking', lazy='select', passive_deletes=True)
