from app.db.database import Base
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, relationship, mapped_column
import uuid

class CoupleMember(Base):
    __tablename__ = "couple_members"
    
    id: Mapped[int] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    
    user_id: Mapped[str] = mapped_column()