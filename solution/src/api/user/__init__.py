from fastapi import APIRouter

from src.api.user.auth import auth_router
from src.api.user.models import User

user_router = APIRouter(prefix="/user", tags=["user"])

user_router.include_router(auth_router)
