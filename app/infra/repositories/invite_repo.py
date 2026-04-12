from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.domain.models.invite import Invite 

class InviteRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def create(self, couple_id: str, invited_by: str, token: str, expires_at: datetime)-> Invite:
        invite = Invite(
            couple_id=couple_id,
            invited_by=invited_by,
            token=token,
            expires_at=expires_at
        )
        self.db.add(invite)
        self.db.commit()
        self.db.refresh(invite)
        return invite
    
    def get_by_token(self, token: str) -> Invite | None:
        return self.db.query(Invite).filter(Invite.token == token).first()
    
    def mark_used(self, invite: Invite) -> None:
        invite.is_used = True
        self.db.commit()