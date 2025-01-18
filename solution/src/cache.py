from typing import Any

from redis import Redis

from src.config import settings

redis = Redis(settings.REDIS_HOST, settings.REDIS_PORT)

CACHE_KEYS_SEPARATOR = ":"


def separate(*args: Any):
    return CACHE_KEYS_SEPARATOR.join(args)


__all__ = [
    "redis",
]
