import enum
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import BigInteger, String, SmallInteger, Numeric, Date, CheckConstraint, UniqueConstraint, Index, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db
from app.models._mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.hostel import Hostel
    from app.models.booking import Booking

class AvailabilityStatus(str, enum.Enum):
    AVAILABLE = 'available'
    UNAVAILABLE = 'unavailable'
    MAINTENANCE = 'maintenance'

class Room(TimestampMixin, db.Model):
    __tablename__ = 'rooms'
    __table_args__ = (
        UniqueConstraint('hostel_id', 'room_number', name='uq_rooms_hostel_room_number'),
        CheckConstraint('capacity > 0', name='ck_rooms_capacity'),
        CheckConstraint('price_per_night >= 0', name='ck_rooms_price'),
        Index('ix_rooms_hostel_status', 'hostel_id', 'availability_status'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    hostel_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('hostels.id', ondelete='CASCADE'), nullable=False)
    room_number: Mapped[str] = mapped_column(String(30), nullable=False)
    room_type: Mapped[Optional[str]] = mapped_column(String(50))
    capacity: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    price_per_night: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    availability_status: Mapped[str] = mapped_column(String(20), nullable=False, default=AvailabilityStatus.AVAILABLE.value)

    hostel: Mapped['Hostel'] = relationship('Hostel', back_populates='rooms')
    bookings: Mapped[List['Booking']] = relationship('Booking', back_populates='room', lazy='select')
    blocks: Mapped[List['RoomBlock']] = relationship('RoomBlock', back_populates='room', lazy='select', passive_deletes=True)

class RoomBlock(TimestampMixin, db.Model):
    __tablename__ = 'room_blocks'
    __table_args__ = (
        CheckConstraint('end_date > start_date', name='ck_room_blocks_dates'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    room_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('rooms.id', ondelete='CASCADE'), nullable=False, index=True)
    start_date: Mapped[object] = mapped_column(Date, nullable=False)
    end_date: Mapped[object] = mapped_column(Date, nullable=False)
    reason: Mapped[Optional[str]] = mapped_column(String(200))

    room: Mapped['Room'] = relationship('Room', back_populates='blocks')
