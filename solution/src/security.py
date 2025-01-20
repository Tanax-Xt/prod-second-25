from datetime import datetime, timedelta, timezone
from hashlib import sha256

import jwt

from src.api.schemas import JWT, Token
from src.config import settings


def create_access_token(subject: int | str, secret: str, minutes: int = settings.JWT_EXPIRE_MINUTES) -> Token:
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=minutes)
    to_encode = JWT(exp=expires_at, sub=subject)
    access_token = jwt.encode(to_encode.model_dump(), secret, algorithm=settings.JWT_ALGORITHM)
    return Token(token=access_token, expires_at=expires_at)


def is_valid_password(plain_password: str, hashed_password: str) -> bool:
    return sha256(plain_password.encode('utf-8')).hexdigest() == hashed_password


def get_password_hash(password: str) -> str:
    return sha256(password.encode('utf-8')).hexdigest()
