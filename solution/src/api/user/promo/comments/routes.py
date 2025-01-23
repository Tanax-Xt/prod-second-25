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
from src.api.user.promo.comments.schemas import CommentText, CommentResponse
from src.api.user.promo.comments.service import create_comment, comment_to_response
from src.db.deps import Session

comments_router = APIRouter(prefix="/{id}/comments")


@comments_router.post("", status_code=status.HTTP_200_OK, response_model=CommentResponse, response_model_exclude_none=True)
async def add_comment(id: uuid.UUID,
                      schema: CommentText,
                      Authorization: str = Header(None),
                      session: Session = Session):
    if not Authorization or not Authorization.startswith("Bearer "):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or missing Authorization header")

    user = get_user_by_token(Authorization, session)
    promo = get_promo_by_id(id, session)

    if promo is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Промокод не найден.")

    comment = create_comment(session, promo, user, schema)

    return comment_to_response(comment)

    # if promo.business_id != business.id:
    #     raise HTTPException(status.HTTP_403_FORBIDDEN, "Промокод не принадлежит этой компании.")

# @promo_router.get("/{id}", status_code=status.HTTP_200_OK, response_model=PromoForUser,
#                   response_model_exclude_none=True)
# async def promo_list(id: uuid.UUID,
#                      Authorization: str = Header(None),
#                      session: Session = Session):
#     if not Authorization or not Authorization.startswith("Bearer "):
#         raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or missing Authorization header")
#
#     user = get_user_by_token(Authorization, session)
#     promo = get_promo_by_id(id, session)
#
#     if promo is None:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, "Промокод не найден.")
#
#     return promo_to_response_for_user(promo, user, session)
#
#
# @promo_router.post("/{id}/like", status_code=status.HTTP_200_OK,
#                    response_model_exclude_none=True)
# async def add_like(id: uuid.UUID,
#                    Authorization: str = Header(None),
#                    session: Session = Session):
#     if not Authorization or not Authorization.startswith("Bearer "):
#         raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or missing Authorization header")
#
#     user = get_user_by_token(Authorization, session)
#     promo = get_promo_by_id(id, session)
#
#     if promo is None:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, "Промокод не найден.")
#
#     add_like_to_promo_by_user(user, promo, session)
#     return {"status": "ok"}
#
#
# @promo_router.delete("/{id}/like", status_code=status.HTTP_200_OK,
#                      response_model_exclude_none=True)
# async def delete_like(id: uuid.UUID,
#                       Authorization: str = Header(None),
#                       session: Session = Session):
#     if not Authorization or not Authorization.startswith("Bearer "):
#         raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or missing Authorization header")
#
#     user = get_user_by_token(Authorization, session)
#     promo = get_promo_by_id(id, session)
#
#     if promo is None:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, "Промокод не найден.")
#
#     delete_like_to_promo_by_user(user, promo, session)
#     return {"status": "ok"}
