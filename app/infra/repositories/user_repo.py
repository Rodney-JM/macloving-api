from sqlalchemy.orm import Session
from app.domain.models.user import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def get_by_id(self, user_id: str) -> User | None:
        return self.db.get(User, user_id)
    
    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()
    
    def email_exists(self, email: str) ->bool:
        return self.db.query(User.id).filter(User.email == email).first() is not None
    
    def create(self, name: str, email: str, password_hash: str) -> User:
        user = User(name=name, email=email, password_hash=password_hash)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user