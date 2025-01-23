"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "fusion" by Rapid Integration (https://github.com/rapid-integration).
Available at: https://github.com/rapid-integration/fusion

This code may be based on "api" by Quotepedia (https://github.com/quotepedia).
Available at: https://github.com/quotepedia/api

Modifications made by Danila Sedelnikov on January 2025.
"""

from datetime import timedelta

from redis.typing import KeyT, ResponseT

from src.cache import redis, separate
from src.config import settings


def set_secret(id: str, secret: str, prefix: str):
    name = generate_code_cache_name(prefix, id)
    expires_at = timedelta(minutes=settings.JWT_EXPIRE_MINUTES)

    redis.set(name, secret, expires_at)


def set_secret_with_timedelta(id: str, secret: str, prefix: str, timedelta: timedelta):
    name = generate_code_cache_name(prefix, id)
    redis.set(name, secret, timedelta)


def get_secret(id: str, prefix: str) -> ResponseT:
    name = generate_code_cache_name(prefix, id)
    secret = redis.get(name)

    return secret


def generate_code_cache_name(prefix: str, subject: str) -> KeyT:
    return separate(prefix, subject)
