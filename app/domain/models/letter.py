import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Index, ForeignKey, Index, Integer, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime

from app.infra.db.base import (
    Base,
    TimestampMixin, 
    UUIDMixin
)

from app.domain.enums.letter_status import LetterStatus

class Letter(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "letters"
    __table_args__ = (
        Index("ix_letters_couple_id", "couple_id"),
        Index("ix_letters_recipient_id", "recipient_id")
    )
    
    couple_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("couples.id", ondelete="CASCADE"),
        nullable=False
    )
    author_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    recipient_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    body: Mapped[str] = mapped_column(
        Text, nullable=False
    )
    status: Mapped[LetterStatus] = mapped_column(
        String(20),
        default=LetterStatus.DRAFT,
        nullable=False
    )
    sent_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    read_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    
    author: Mapped["User"] = relationship("User", foreign_keys=[author_id])
    recipient: Mapped["User"] = relationship("User", foreign_keys=[recipient_id])