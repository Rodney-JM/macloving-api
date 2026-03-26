from db.database import Base
from app.enums.relationship_status import RelationshipStatus
from app.enums.subscription_status import SubscriptionStatus
from sqlalchemy import ForeignKey, func, String, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid

class Couple(Base):
    __tablename__ = "couples"
    
    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str | None] = mapped_column(String(150), nullable=True)
    relationship_start_date: Mapped[DateTime | None] = mapped_column(nullable=True)
    relationship_status: Mapped[RelationshipStatus] = mapped_column(
        Enum(RelationshipStatus),
        default=RelationshipStatus.dating
    )
    
    cover_image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    invite_code: Mapped[str] = mapped_column(
        String(20),
        unique=True, 
        default=lambda: str(uuid.uuid4())[:8]
    )
    
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True, server_default=func.now())
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
        onupdate=func.now()
    )
    
    subscription_status: Mapped[SubscriptionStatus] = mapped_column(
        Enum(SubscriptionStatus),
        default=SubscriptionStatus.free
    )
    subscription_expires_at: Mapped[DateTime | None] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    
    members: Mapped[list["CoupleMember"]] = relationship(back_populates="couple")