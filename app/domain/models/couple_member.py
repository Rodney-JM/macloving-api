from app.infra.db.database import Base
from sqlalchemy import String, DateTime, func, ForeignKey, Enum
from sqlalchemy.orm import Mapped, relationship, mapped_column
from app.domain.enums.member_role import MemberRole
import uuid

class CoupleMember(Base):
    __tablename__ = "couple_members"
    
    id: Mapped[int] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    
    # Estrutura do banco mesmo
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    couple_id: Mapped[str] = mapped_column(ForeignKey("couples.id"))
    
    role: Mapped[MemberRole] = mapped_column(
        Enum(MemberRole), default=MemberRole.partner
    )
    
    joined_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    
    # Objetos pra ajd no Python
    user: Mapped["User"] = relationship(back_populates="couples")
    couple: Mapped["Couple"] = relationship(back_populates="members")