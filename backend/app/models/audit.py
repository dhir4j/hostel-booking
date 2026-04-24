from datetime import datetime
from typing import Optional, Any
from sqlalchemy import BigInteger, String, DateTime, func, Index, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    __table_args__ = (
        Index('ix_audit_logs_entity', 'entity_type', 'entity_id'),
        Index('ix_audit_logs_actor', 'actor_user_id'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    actor_user_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False)
    entity_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    action: Mapped[str] = mapped_column(String(50), nullable=False)
    # IMPORTANT: Python attribute 'extra' maps to DB column 'metadata'
    extra: Mapped[Optional[Any]] = mapped_column('metadata', JSONB, nullable=True)
    ip: Mapped[Optional[str]] = mapped_column(String(45))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
