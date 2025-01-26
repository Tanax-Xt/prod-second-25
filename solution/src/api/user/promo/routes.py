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

from fastapi import APIRouter, status, Header, HTTPException, Depends, Response

from src.api.business.promo.service import get_promo_by_id, is_promo_is_active_on_cur_date
from src.api.user.auth.service import get_user_by_token
from src.api.user.feed.schemas import PromoForUser
from src.api.user.feed.service import promo_to_response_for_user
from src.api.user.promo.comments.schemas import CommentsToUserSearchParams
from src.api.user.promo.services import add_like_to_promo_by_user, delete_like_to_promo_by_user, \
    is_correct_antifraud_status, get_promo_var, is_user_fits_to_target, get_user_activations_history
from src.db.deps import Session

promo_router = APIRouter(prefix="/promo")


@promo_router.get("/history", status_code=status.HTTP_200_OK, response_model=list[PromoForUser],
                  response_model_exclude_none=True)
async def promo_list(response: Response,
                     query: CommentsToUserSearchParams = Depends(CommentsToUserSearchParams),
                     Authorization: str = Header(None),
                     session: Session = Session):
    if not Authorization or not Authorization.startswith("Bearer "):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or missing Authorization header")

    user = get_user_by_token(Authorization, session)

    promos, total_count = get_user_activations_history(user, session, query)
    response.headers["X-Total-Count"] = str(total_count)

    return [promo_to_response_for_user(promo, user, session) for promo in promos]


@promo_router.get("/{id}", status_code=status.HTTP_200_OK, response_model=PromoForUser,
                  response_model_exclude_none=True)
async def get_promo(id: uuid.UUID,
                    Authorization: str = Header(None),
                    session: Session = Session):
    if not Authorization or not Authorization.startswith("Bearer "):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or missing Authorization header")

    user = get_user_by_token(Authorization, session)
    promo = get_promo_by_id(id, session)

    if promo is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Промокод не найден.")

    return promo_to_response_for_user(promo, user, session)


@promo_router.post("/{id}/like", status_code=status.HTTP_200_OK,
                   response_model_exclude_none=True)
async def add_like(id: uuid.UUID,
                   Authorization: str = Header(None),
                   session: Session = Session):
    if not Authorization or not Authorization.startswith("Bearer "):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or missing Authorization header")

    user = get_user_by_token(Authorization, session)
    promo = get_promo_by_id(id, session)

    if promo is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Промокод не найден.")

    add_like_to_promo_by_user(user, promo, session)
    return {"status": "ok"}


@promo_router.delete("/{id}/like", status_code=status.HTTP_200_OK,
                     response_model_exclude_none=True)
async def delete_like(id: uuid.UUID,
                      Authorization: str = Header(None),
                      session: Session = Session):
    if not Authorization or not Authorization.startswith("Bearer "):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or missing Authorization header")

    user = get_user_by_token(Authorization, session)
    promo = get_promo_by_id(id, session)

    if promo is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Промокод не найден.")

    delete_like_to_promo_by_user(user, promo, session)
    return {"status": "ok"}


@promo_router.post("/{id}/activate", status_code=status.HTTP_200_OK,
                   response_model_exclude_none=True)
async def activate_promo(id: uuid.UUID, Authorization: str = Header(None), session: Session = Session):
    if not Authorization or not Authorization.startswith("Bearer "):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or missing Authorization header")

    user = get_user_by_token(Authorization, session)
    promo = get_promo_by_id(id, session)

    if promo is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Промокод не найден.")

    if not is_promo_is_active_on_cur_date(promo, session):
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    if not is_user_fits_to_target(user, promo):
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    if not is_correct_antifraud_status(user, promo):
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    user_promo_var = get_promo_var(user, promo, session)

    if user_promo_var is None:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    return {"promo": user_promo_var}
