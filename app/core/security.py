import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional, Any
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings
from uuid import UUID
import bleach

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


_ALLOWED_TAGS: list[str] = []
_ALLOWED_ATTRS: dict = {}

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def sanitize_input(value: str) -> str:
    return bleach.clean(value, tags=_ALLOWED_TAGS, attributes=_ALLOWED_ATTRS, strip=True)


def _create_token(
    subject: str | UUID,
    expires_delta: timedelta,
    token_type: str,
    extra_claims: dict[str, Any] | None = None
) -> str:
    now = datetime.now(timezone.utc)
    expire = now + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    payload = {
        "sub": str(subject), 
        "exp": expire, 
        "iat": now,
        "type": token_type
    }
    if extra_claims:
        payload.update(extra_claims)
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    
def create_access_token(subject: str | UUID, couple_id: UUID | None = None , expires_delta: Optional[timedelta] = None) -> str:
    extra = dict[str, Any] = {}
    if couple_id: 
        extra["couple_id"] = str(couple_id)
    expires = expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return _create_token(subject, expires, "access", extra_claims=extra)
    
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


#getting users
def get_user_id_from_token(token: str) -> UUID:
    payload = verify_token(token, token_type="access")
    return UUID(payload["sub"])

def get_couple_id_from_token(token: str)-> UUID| None:
    payload = verify_token(token, token_type="access")
    raw = payload.get("couple_id")
    return UUID(raw) if raw else None