import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Text, DateTime, Date, ForeignKey, func, Index, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infra.db.base import (
    Base, 
    UUIDMixin,
    TimestampMixin
)
from app.domain.enums.memory_category import MemoryCategory

class Memory(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "memories"
    __table_args__ = (
        Index("ix_memories_album_id", "album_id"),
        Index("ix_memories_author_id", "author_id"),
        Index("ix_memories_couple_id", "couple_id")
    )
    
    album_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("albums.id", ondelete="CASCADE"),
        nullable=False
    )
    author_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=False
    )
    couple_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("couples.id", ondelete="CASCADE"),
        nullable=False
    )
    
    title: Mapped[str | None] = mapped_column(String(200), nullable=True)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    memory_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    
    media_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    thumbnail_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    media_type: Mapped[str | None] = mapped_column(String(20), nullable=True)
    
    #s3ref
    s3_key: Mapped[str] = mapped_column(String(512), nullable=False)
    s3_thumbnail_key: Mapped[str | None] = mapped_column(String(512), nullable=True)
    
    #metadata
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    caption: Mapped[str | None] = mapped_column(String(500), nullable=True)
    category: Mapped[MemoryCategory] = mapped_column(
        String(30), default=MemoryCategory.OTHER, nullable=False
    )
    file_size_bytes: Mapped[int] = mapped_column(BigInteger, nullable=False)
    width: Mapped[int | None] = mapped_column(nullable=True)
    height: Mapped[int | None] = mapped_column(nullable=True)
    taken_at: Mapped[str | None] = mapped_column(String(30), nullable=True)
    
    album: Mapped["Album"] = relationship(back_populates="memories", foreign_keys=[album_id])
    author: Mapped["User"] = relationship(back_populates="memories", foreign_keys=[author_id])