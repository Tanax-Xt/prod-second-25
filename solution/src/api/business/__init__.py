from fastapi import APIRouter

from src.api.business.auth import auth_router
from src.api.business.models import Business
from src.api.business.promo import promo_router

business_router = APIRouter(prefix="/business", tags=["business"])

business_router.include_router(auth_router)
business_router.include_router(promo_router)
