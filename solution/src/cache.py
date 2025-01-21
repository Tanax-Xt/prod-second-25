"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "fusion" by Rapid Integration (https://github.com/rapid-integration).
Available at: https://github.com/rapid-integration/fusion

This code may be based on "api" by Quotepedia (https://github.com/quotepedia).
Available at: https://github.com/quotepedia/api

Modifications made by Danila Sedelnikov on January 2025.
"""

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
