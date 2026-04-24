import enum
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import BigInteger, String, Text, Boolean, Numeric, Table, Column, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db
from app.models._mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.room import Room
    from app.models.booking import Booking

class HostelStatus(str, enum.Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'

# Association table for many-to-many hostel <-> amenity
hostel_amenities = Table(
    'hostel_amenities',
    db.metadata,
    Column('hostel_id', BigInteger, ForeignKey('hostels.id', ondelete='CASCADE'), primary_key=True),
    Column('amenity_id', BigInteger, ForeignKey('amenities.id', ondelete='CASCADE'), primary_key=True),
)

class Hostel(TimestampMixin, db.Model):
    __tablename__ = 'hostels'
    __table_args__ = (
        Index('ix_hostels_city', 'city'),
        Index('ix_hostels_status', 'status'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    admin_user_id: Mapped[int] = mapped_column(BigInteger, db.ForeignKey('users.id', ondelete='RESTRICT'), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    city: Mapped[str] = mapped_column(String(80), nullable=False)
    address: Mapped[str] = mapped_column(Text, nullable=False)
    latitude: Mapped[Optional[float]] = mapped_column(Numeric(9, 6))
    longitude: Mapped[Optional[float]] = mapped_column(Numeric(9, 6))
    status: Mapped[str] = mapped_column(String(20), nullable=False, default=HostelStatus.ACTIVE.value)
    auto_approve: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    admin_user: Mapped['User'] = relationship('User', back_populates='hostels')
    rooms: Mapped[List['Room']] = relationship('Room', back_populates='hostel', lazy='select', passive_deletes=True)
    images: Mapped[List['HostelImage']] = relationship('HostelImage', back_populates='hostel', lazy='select', passive_deletes=True)
    amenities: Mapped[List['Amenity']] = relationship('Amenity', secondary=hostel_amenities, lazy='select')
    bookings: Mapped[List['Booking']] = relationship('Booking', back_populates='hostel', lazy='select')

class HostelImage(TimestampMixin, db.Model):
    __tablename__ = 'hostel_images'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    hostel_id: Mapped[int] = mapped_column(BigInteger, db.ForeignKey('hostels.id', ondelete='CASCADE'), nullable=False, index=True)
    image_url: Mapped[str] = mapped_column(Text, nullable=False)
    is_primary: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    sort_order: Mapped[int] = mapped_column(db.Integer, nullable=False, default=0)

    hostel: Mapped['Hostel'] = relationship('Hostel', back_populates='images')

class Amenity(db.Model):
    __tablename__ = 'amenities'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    hostels: Mapped[List['Hostel']] = relationship('Hostel', secondary=hostel_amenities, back_populates='amenities', lazy='select')
