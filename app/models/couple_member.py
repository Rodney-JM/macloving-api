from app.db.database import Base
from sqlalchemy import String, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
import uuid

class CoupleMember(Base):
    __tablename__ = "couple_members"
    
    id: Mapped[int] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    
    # Estrutura do banco mesmo
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    couple_id: Mapped[str] = mapped_column(ForeignKey("couples.id"))
    
    # Objetos pra ajd no Python
    user: Mapped["User"] = relationship(back_populates="couples")
    couple: Mapped["Couple"] = relationship(back_populates="members")