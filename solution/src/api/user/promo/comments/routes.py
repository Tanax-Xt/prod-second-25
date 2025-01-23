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

from src.api.business.promo.service import get_promo_by_id
from src.api.user.auth.service import get_user_by_token
from src.api.user.promo.comments.schemas import CommentText, CommentResponse, CommentsToUserSearchParams
from src.api.user.promo.comments.service import create_comment, comment_to_response, get_comment_by_id, delete_comment, \
    update_comment, get_comments_by_promo
from src.db.deps import Session

comments_router = APIRouter(prefix="/comments")


@comments_router.post("", status_code=status.HTTP_200_OK, response_model=CommentResponse,
                      response_model_exclude_none=True)
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


@comments_router.get("", status_code=status.HTTP_200_OK, response_model=list[CommentResponse],
                     response_model_exclude_none=True)
async def get_comments_list(id: uuid.UUID,
                            response: Response,
                            query: CommentsToUserSearchParams = Depends(CommentsToUserSearchParams),
                            Authorization: str = Header(None),
                            session: Session = Session):
    if not Authorization or not Authorization.startswith("Bearer "):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or missing Authorization header")

    # user = get_user_by_token(Authorization, session)
    promo = get_promo_by_id(id, session)

    if promo is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Промокод не найден.")

    comments, total_count = get_comments_by_promo(promo, query)
    response.headers["X-Total-Count"] = str(total_count)

    return comments


@comments_router.get("/{comment_id}", status_code=status.HTTP_200_OK, response_model=CommentResponse,
                     response_model_exclude_none=True)
async def get_comment(id: uuid.UUID,
                      comment_id: uuid.UUID,
                      Authorization: str = Header(None),
                      session: Session = Session):
    if not Authorization or not Authorization.startswith("Bearer "):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or missing Authorization header")

    promo = get_promo_by_id(id, session)

    if promo is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Промокод не найден.")

    comment = get_comment_by_id(comment_id, promo, session)

    if comment is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Комментарий не найден.")

    return comment_to_response(comment)


@comments_router.put("/{comment_id}", status_code=status.HTTP_200_OK, response_model=CommentResponse,
                     response_model_exclude_none=True)
async def put_comment(id: uuid.UUID,
                      schema: CommentText,
                      comment_id: uuid.UUID,
                      Authorization: str = Header(None),
                      session: Session = Session):
    if not Authorization or not Authorization.startswith("Bearer "):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or missing Authorization header")

    user = get_user_by_token(Authorization, session)

    promo = get_promo_by_id(id, session)

    if promo is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Промокод не найден.")

    comment = get_comment_by_id(comment_id, promo, session)

    if comment is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Комментарий не найден.")

    if comment.author != user:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Комментарий не принадлежит пользователю.")

    comment = update_comment(comment, schema, session)

    return comment_to_response(comment)


@comments_router.delete("/{comment_id}", status_code=status.HTTP_200_OK,
                        response_model_exclude_none=True)
async def del_comment(id: uuid.UUID,
                      comment_id: uuid.UUID,
                      Authorization: str = Header(None),
                      session: Session = Session):
    if not Authorization or not Authorization.startswith("Bearer "):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or missing Authorization header")

    user = get_user_by_token(Authorization, session)

    promo = get_promo_by_id(id, session)

    if promo is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Промокод не найден.")

    comment = get_comment_by_id(comment_id, promo, session)

    if comment is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Комментарий не найден.")

    if comment.author != user:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Комментарий не принадлежит пользователю.")

    delete_comment(comment, session)

    return {"status": "ok"}
