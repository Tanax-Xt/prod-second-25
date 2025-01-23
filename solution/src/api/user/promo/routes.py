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

from fastapi import APIRouter, status, Header, HTTPException

from src.api.business.promo.service import get_promo_by_id
from src.api.user.auth.service import get_user_by_token
from src.api.user.feed.schemas import PromoForUser
from src.api.user.feed.service import promo_to_response_for_user
from src.db.deps import Session

promo_router = APIRouter(prefix="/promo")


@promo_router.get("/{id}", status_code=status.HTTP_200_OK, response_model=PromoForUser,
                  response_model_exclude_none=True)
async def promo_list(id: uuid.UUID,
                     Authorization: str = Header(None),
                     session: Session = Session):
    if not Authorization or not Authorization.startswith("Bearer "):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or missing Authorization header")

    user = get_user_by_token(Authorization, session)
    promo = get_promo_by_id(id, session)

    if promo is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Промокод не найден.")

    return promo_to_response_for_user(promo, user)
