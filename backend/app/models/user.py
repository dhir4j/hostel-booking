import enum
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import BigInteger, String, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db
from app.models._mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.hostel import Hostel
    from app.models.booking import Booking
    from app.models.auth_token import AuthToken, PasswordReset
    from app.models.audit import AuditLog

class UserRole(str, enum.Enum):
    USER = 'user'
    ADMIN = 'admin'

class User(TimestampMixin, db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    phone: Mapped[Optional[str]] = mapped_column(String(30))
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False, default=UserRole.USER.value)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    # Relationships
    bookings: Mapped[List['Booking']] = relationship('Booking', back_populates='user', lazy='select')
    auth_tokens: Mapped[List['AuthToken']] = relationship('AuthToken', back_populates='user', lazy='select')
    password_resets: Mapped[List['PasswordReset']] = relationship('PasswordReset', back_populates='user', lazy='select')
    admin_profile: Mapped[Optional['AdminProfile']] = relationship('AdminProfile', back_populates='user', uselist=False, lazy='select')
    hostels: Mapped[List['Hostel']] = relationship('Hostel', back_populates='admin_user', lazy='select')

class AdminProfile(TimestampMixin, db.Model):
    __tablename__ = 'admin_profiles'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    organization: Mapped[Optional[str]] = mapped_column(String(150))

    user: Mapped['User'] = relationship('User', back_populates='admin_profile')
