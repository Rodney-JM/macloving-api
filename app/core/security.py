import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def _create_token(subject: str, expires_delta: timedelta, token_type: str) -> str:
    now = datetime.now(timezone.utc)
    expire = now + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    payload = {
        "sub": str(subject), 
        "exp": expire, 
        "iat": now,
        "type": token_type
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    
def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    expires = expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return _create_token(subject, expires, "access")
    
def create_refresh_token(subject: str) -> str:
    expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    return _create_token(subject, expires, "refresh")
    
def create_password_reset_token(email: str) -> str:
    expires = timedelta(hours=24)
    return _create_token(email, expires, "reset")


""" def create_password_reset_token(email: str) -> str:
    delta = timedelta(hours=24)
    now = datetime.utcnow()
    expires = now + delta
    to_encode = {"exp": expires, "sub": email, "type": "reset", "nbf": now}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM) """
    
    

def verify_token(token: str, token_type: str = "access") -> Optional[str]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != token_type:
            return None
        subject: Optional[str] = payload.get("sub")
        return subject
    except JWTError:
        return None


def generate_secure_filename(original_file_name: str) -> str:
    if "." in original_file_name:
        ext  = original_file_name.rsplit(".", 1)[-1].lower()
    else:
        ext = ""
        
    if ext and ext not in settings.ALLOWED_EXTENSIONS:
        raise ValueError("Extensão de arquivo não permitida")
    
    random_name = secrets.token_urlsafe(16)
    
    return f"{random_name}.{ext}" if ext else random_name