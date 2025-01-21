"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "fusion" by Rapid Integration (https://github.com/rapid-integration).
Available at: https://github.com/rapid-integration/fusion

This code may be based on "api" by Quotepedia (https://github.com/quotepedia).
Available at: https://github.com/quotepedia/api

Modifications made by Danila Sedelnikov on January 2025.
"""

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
