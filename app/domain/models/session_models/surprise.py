import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.domain.enums.surprise_enums import *

from app.infra.db.base import Base, TimestampMixin, UUIDMixin

class Surprise(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "surprises"
    __table_args__ = (
        Index("ix_surprises_couple_id", "couple_id"),
        Index("ix_surprises_recipient_id", "recipient_id"),
        Index("ix_surprises_unlocks_at", "unlocks_at")
    )
    
    couple_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("couples.id", ondelete="CASCADE"), nullable=False
    )
    sender_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    recipient_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    surprise_type: Mapped[SurpriseType] = mapped_column(String(30), nullable=False)
    status: Mapped[SurpriseStatus] = mapped_column(String(20), default=SurpriseStatus.PENDING, nullable=False)
    
    #optional time lock
    unlocks_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    opened_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    
    #optinal media
    media_s3_key: Mapped[str | None] = mapped_column(String(512), nullable=True)
    
    sender: Mapped["User"] = relationship("User", foreign_keys=[sender_id])
    recipient: Mapped["User"] = relationship("User", foreign_keys=[recipient_id])