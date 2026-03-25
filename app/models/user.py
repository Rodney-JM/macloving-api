from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
import uuid

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[str] = mapped_column(
       String(36), primary_key=True, default=lambda: str(uuid.uuid4()) 
    )
    
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True, server_default=func.now())
    )
    is_active: Mapped[bool]
    
    couples: Mapped[list["CoupleMember"]] = relationship(back_populates="user")
    
    albums: Mapped[list["AlbumMember"]] = relationship(back_populates="user")