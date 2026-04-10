""" from sqlalchemy.orm import Session
from app.core.config import settings
from typing import Generator
from app.db.database import SessionLocal
from app.core.security import verify_token
from app.core.exceptions import UnauthorizedError
from app.models.user import User

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

#Sessao
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# Auth
bearer_scheme = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)) -> User:
    #extrai e valida o JWT
    user_id = verify_token(credentials.credentials, token_type="access")
    if not user_id:
        raise UnauthorizedError("Token inválido ou expirado")
    
    user = db.get(User, user_id)
    if not user or not user.is_active:
        raise UnauthorizedError("Usuário não encontrado ou inativo.")
    
    return user """