from fastapi import APIRouter

from src.api import business
from src.api import ping

api_router = APIRouter(prefix="/api")

api_router.include_router(ping.router)
api_router.include_router(business.business_router)

__all__ = [
    "api_router",
]
