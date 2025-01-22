from fastapi import APIRouter

from src.api.user.auth import auth_router
from src.api.user.models import User
from src.api.user.profile import profile_router
from src.api.user.feed import feed_router
from src.api.user.promo import promo_router

user_router = APIRouter(prefix="/user", tags=["user"])

user_router.include_router(auth_router)
user_router.include_router(profile_router)
user_router.include_router(feed_router)
user_router.include_router(promo_router)