from datetime import datetime, timedelta

import bcrypt
from jose import jwt, JWTError

from app.core.config import settings


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode(), password_hash.encode())


def create_access_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.token_expire_minutes)
    data = {"sub": str(user_id), "exp": expire}
    return jwt.encode(data, settings.secret_key, algorithm=settings.algorithm)


def decode_access_token(token: str):
    """Returns the user id from the token, or None if the token is bad."""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return int(payload["sub"])
    except (JWTError, KeyError, ValueError):
        return None