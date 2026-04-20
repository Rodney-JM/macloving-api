import uuid
from datetime import date, datetime

from sqlalchemy import Boolean, Date, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.enums.ritual_status import RitualStatus
from app.infra.db.base import (
    Base,
    UUIDMixin,
    TimestampMixin
)

class Ritual(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "rituals"
    __table_args__ = (Index("ix_rituals_couple_id", "couple_id"))
    
    couple_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("couples.id", ondelete="CASCADE"),
        nullable=False
    )
    created_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("couples.id", ondelete="CASCADE"),
        nullable=False
    )
    
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(300), nullable=False)
    icon: Mapped[str] = mapped_column(String(10), default="✨", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    current_streak: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    longest_streak: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    entries: Mapped[list["RitualEntry"]] = relationship(
        "RitualEntry",
        back_populates="ritual",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    def __repr__(self) -> str:
        return f"<Ritual '{self.title}'>"