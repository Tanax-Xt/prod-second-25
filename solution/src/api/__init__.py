from fastapi import APIRouter
from src.api import ping

api_router = APIRouter(prefix="/api")

api_router.include_router(ping.router)

__all__ = [
    "api_router",
]