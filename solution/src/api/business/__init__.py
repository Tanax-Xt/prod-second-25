from fastapi import APIRouter

from src.api.business.auth import auth_router
from src.api.business.models import Business

business_router = APIRouter(prefix="/business", tags=["business"])

business_router.include_router(auth_router)
