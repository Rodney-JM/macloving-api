from datetime import datetime, timedelta, timezone
from typing import Any
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(subject: Any, expires_delta: timedelta | None = None) -> str:
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {"sub": str(subject), "exp": expire}
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    )
    
    def create_refresh_token(subject: Union[str, Any]) -> str:
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_password_reset_token(email: str) -> str:
    delta = timedelta(hours=24)
    now = datetime.utcnow()
    expires = now + delta
    to_encode = {"exp": expires, "sub": email, "type": "reset", "nbf": now}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def verify_token(token: str, token_type: str = "access") -> Optional[str]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != token_type:
            return None
        subject: str = payload.get("sub")
        return subject
    except JWTError:
        return None


def generate_secure_filename(original_filename: str) -> str:
    ext = original_filename.rsplit(".", 1)[-1].lower() if "." in original_filename else ""
    random_name = secrets.token_urlsafe(16)
    return f"{random_name}.{ext}" if ext else random_name