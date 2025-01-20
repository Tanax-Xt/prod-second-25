import uuid

from fastapi import APIRouter, status, Header, HTTPException

from src.api.business.auth.service import get_business_by_token
from src.api.business.promo.schemas import PromoCreate, PromoResponse
from src.api.business.promo.service import create_promo, get_promo_by_id, promo_to_response
from src.db.deps import Session

promo_router = APIRouter(prefix="/promo", tags=["business-promo"])


@promo_router.post("", status_code=status.HTTP_201_CREATED)
async def promo(promo: PromoCreate, Authorization: str = Header(), session: Session = Session):
    if not Authorization or not Authorization.startswith("Bearer "):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or missing Authorization header")

    business = get_business_by_token(Authorization, session)
    promo = create_promo(session, promo, business)
    return {"id": promo.id}


# @promo_router.get("", status_code=status.HTTP_200_OK, response_model=list[PromoResponse])
# async def promo_list(Authorization: str = Header(), session: Session = Session):
#     pass


@promo_router.get("/{id}", status_code=status.HTTP_200_OK, response_model=PromoResponse,
                  response_model_exclude_none=True)
async def get_promo(id: uuid.UUID, Authorization: str = Header(), session: Session = Session):
    if not Authorization or not Authorization.startswith("Bearer "):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or missing Authorization header")

    business = get_business_by_token(Authorization, session)
    promo = get_promo_by_id(id, session)

    if promo is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Промокод не найден.")

    if promo.business_id != business.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Промокод не принадлежит этой компании.")

    return promo_to_response(promo)

# @promo_router.patch("/{id}", status_code=status.HTTP_200_OK)
# async def patch_promo(id: str):
#     pass
