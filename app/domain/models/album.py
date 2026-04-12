from sqlalchemy import String, ForeignKey, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infra.db.database import Base
import uuid

class Album(Base):
    __tablename__ = "albums"
    
    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    couple_id: Mapped[str] = mapped_column(
        ForeignKey("couples.id"), index=True
    )
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    cover_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    
    couple: Mapped["Couple"] = relationship(back_populates="albums")
    memories: Mapped[list["Memory"]] = relationship(
        back_populates="album", cascade="all, delete-orphan"
    )
    user: Mapped["User"] = relationship(back_populates="albums")