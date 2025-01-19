from fastapi import APIRouter, status, Header, HTTPException

from src.api.business.auth.service import get_business_by_token
from src.api.business.promo.schemas import PromoCreate
from src.db.deps import Session

promo_router = APIRouter(prefix="/promo", tags=["business-promo"])


@promo_router.post("", status_code=status.HTTP_201_CREATED)
async def create_promo(promo: PromoCreate, Authorization: str = Header(), session: Session = Session):
    if not Authorization or not Authorization.startswith("Bearer "):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or missing Authorization header")

    business = get_business_by_token(Authorization, session)
    return business
