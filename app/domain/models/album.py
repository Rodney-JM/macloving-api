from sqlalchemy import String, ForeignKey, func, DateTime, BigInteger, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.enums.album_category import AlbumCategory
from app.infra.db.base import(
    Base,
    TimestampMixin,
    UUIDMixin
)

import uuid

class AlbumPhoto(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "album_photos"
    
    __table_args = (
        Index("ix_album_photos_couple_id", "couple_id"),
        Index("ix_album_photos_uploaded_by", "uploaded_by"),
        Index("ix_album_photos_category", "category"),
        Index("ix_album_photos_couple_created", "couple_id", "created_at")
    )
    
    couple_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("couples.id", ondelete="CASCADE"),
        nullable=False
    )
    uploaded_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )
    
    #s3ref
    s3_key: Mapped[str] = mapped_column(String(512), nullable=False)
    s3_thumbnail_key: Mapped[str | None] = mapped_column(String(512), nullable=True)
    
    #metadata
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    caption: Mapped[str | None] = mapped_column(String(500), nullable=True)
    category: Mapped[AlbumCategory] = mapped_column(
        String(30), default=AlbumCategory.OTHER, nullable=False
    )
    file_size_bytes: Mapped[int] = mapped_column(BigInteger, nullable=False)
    width: Mapped[int | None] = mapped_column(nullable=True)
    height: Mapped[int | None] = mapped_column(nullable=True)
    taken_at: Mapped[str | None] = mapped_column(String(30), nullable=True)
    
    uploader: Mapped["User"] = relationship("User", foreign_keys=[uploaded_by])
    
    def __repr__(self) -> str:
        return f"<AlbumPhoto {self.original_filename}"