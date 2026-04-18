from sqlalchemy.orm import Session, joinedload
from app.domain.models.couple_models.couple import Couple
from app.domain.models.couple_member import CoupleMember, MemberRole

class CoupleRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def get_by_id(self, couple_id: str) -> Couple | None:
        return (
            self.db.query(Couple)
            .options(joinedload(Couple.members).joinedload(CoupleMember.user))
            .filter(Couple.id == couple_id)
            .first()
        )
    
    def get_couple_of_user(self, user_id: str) -> Couple | None:
        member = (
            self.db.query(CoupleMember)
            .filter(CoupleMember.user_id == user_id)
            .first()
        )
        
        if not member:
            return None
        return self.get_by_id(member.couple_id)
    
    def user_is_member(self, couple_id: str, user_id: str) -> bool:
        return (
            self.db.query(CoupleMember.id)
            .filter(CoupleMember.couple_id == couple_id, CoupleMember.user_id == user_id)
            .first()
        ) is not None
        
    def create(self, owner_id: str) -> Couple:
        couple = Couple()
        self.db.add(Couple)
        self.db.flush()
        member = CoupleMember(couple_id=couple.id, user_id=owner_id, role=MemberRole.owner)
        self.db.add(member)
        self.db.commit()
        self.db.refresh(couple)
        return couple
    
    def add_member(self, couple_id: str, user_id: str) -> CoupleMember:
        member = CoupleMember(couple_id=couple_id, user_id=user_id, role=MemberRole.partner)
        self.db.add(member)
        self.db.commit()
        return member