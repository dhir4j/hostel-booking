from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import BigInteger, Text, DateTime, String, Index, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db
from app.models._mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User

class AuthToken(db.Model):
    __tablename__ = 'auth_tokens'
    __table_args__ = (
        Index('ix_auth_tokens_user_expires', 'user_id', 'revoked_at', 'expires_at'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    refresh_token_hash: Mapped[str] = mapped_column(Text, unique=True, index=True, nullable=False)
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    user_agent: Mapped[Optional[str]] = mapped_column(String(255))
    ip: Mapped[Optional[str]] = mapped_column(String(45))

    user: Mapped['User'] = relationship('User', back_populates='auth_tokens')

class PasswordReset(db.Model):
    __tablename__ = 'password_resets'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    token_hash: Mapped[str] = mapped_column(Text, unique=True, index=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    used_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    user: Mapped['User'] = relationship('User', back_populates='password_resets')
