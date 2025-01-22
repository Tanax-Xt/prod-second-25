"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "fusion" by Rapid Integration (https://github.com/rapid-integration).
Available at: https://github.com/rapid-integration/fusion

This code may be based on "api" by Quotepedia (https://github.com/quotepedia).
Available at: https://github.com/quotepedia/api

Modifications made by Danila Sedelnikov on January 2025.
"""

import uuid

from fastapi import APIRouter, status, Header, HTTPException, Response, Depends

from src.api.business.auth.service import get_business_by_token
from src.api.business.promo.schemas import PromoCreate, PromoResponse, PromosListSearchParams, PromoPatch
from src.api.business.promo.service import create_promo, get_promo_by_id, promo_to_response, \
    get_promos_response_by_business_with_params, update_promo
from src.db.deps import Session

promo_router = APIRouter(prefix="/promo")


@promo_router.post("", status_code=status.HTTP_201_CREATED)
async def promo(promo: PromoCreate, Authorization: str = Header(), session: Session = Session):
    if not Authorization or not Authorization.startswith("Bearer "):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or missing Authorization header")

    business = get_business_by_token(Authorization, session)
    promo = create_promo(session, promo, business)
    return {"id": promo.id}


@promo_router.get("", status_code=status.HTTP_200_OK, response_model=list[PromoResponse],
                  response_model_exclude_none=True)
async def promo_list(response: Response, query: PromosListSearchParams = Depends(PromosListSearchParams),
                     Authorization: str = Header(),
                     session: Session = Session):
    if not Authorization or not Authorization.startswith("Bearer "):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or missing Authorization header")

    business = get_business_by_token(Authorization, session)
    promos, total_count = get_promos_response_by_business_with_params(business, query)
    response.headers["X-Total-Count"] = str(total_count)
    return promos


@promo_router.get("/{id}", status_code=status.HTTP_200_OK, response_model=PromoResponse,
                  response_model_exclude_none=True)
async def get_promo(id: uuid.UUID, Authorization: str = Header(), session: Session = Session) -> PromoResponse:
    if not Authorization or not Authorization.startswith("Bearer "):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or missing Authorization header")

    business = get_business_by_token(Authorization, session)
    promo = get_promo_by_id(id, session)

    if promo is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Промокод не найден.")

    if promo.business_id != business.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Промокод не принадлежит этой компании.")

    return promo_to_response(promo)


@promo_router.patch("/{id}", status_code=status.HTTP_200_OK, response_model=PromoResponse,
                    response_model_exclude_none=True)
async def patch_promo(id: uuid.UUID, schema: PromoPatch, Authorization: str = Header(),
                      session: Session = Session):
    if not Authorization or not Authorization.startswith("Bearer "):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or missing Authorization header")

    business = get_business_by_token(Authorization, session)
    promo = get_promo_by_id(id, session)

    if promo is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Промокод не найден.")

    if promo.business_id != business.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Промокод не принадлежит этой компании.")

    promo = update_promo(promo, schema, session)

    return promo_to_response(promo)
