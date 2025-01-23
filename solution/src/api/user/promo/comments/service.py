"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "fusion" by Rapid Integration (https://github.com/rapid-integration).
Available at: https://github.com/rapid-integration/fusion

This code may be based on "api" by Quotepedia (https://github.com/quotepedia).
Available at: https://github.com/quotepedia/api

Modifications made by Danila Sedelnikov on January 2025.
"""
import datetime
import uuid

from src.api.business.models import Promo
from src.api.user.models import User, Comment
from src.api.user.promo.comments.schemas import CommentText, CommentResponse, Author
from src.db.deps import Session


def create_comment(session: Session, promo: Promo, user: User, schema: CommentText) -> Comment:
    comment = Comment(
        text=schema.text,
        author_id=str(user.id),
        promo_id=str(promo.id)
    )

    session.add(comment)
    session.commit()
    session.refresh(comment)

    return comment


def date_to_RFC_3339(date: datetime.datetime) -> str:
    offset = date.strftime('%z')
    return date.strftime(
        '%Y-%m-%dT%H:%M:%S') + 'Z' + f"{offset[:3] if len(offset) > 0 else '00'}:{offset[3:] if len(offset) > 0 else '00'}"


def comment_to_response(comment: Comment) -> CommentResponse:
    return CommentResponse(
        text=comment.text,
        id=str(comment.id),
        date=date_to_RFC_3339(comment.created_at),
        author=Author(
            name=comment.author.name,
            surname=comment.author.surname,
            image_url=str(comment.author.image_url) if comment.author.image_url is not None else None
        ),
    )


def get_comment_by_id(id: uuid.UUID, promo: Promo, session: Session) -> Comment:
    return session.query(Comment).filter(((Comment.id == id) & (Comment.promo_id == promo.id))).first()


def delete_comment(comment: Comment, session: Session):
    session.delete(comment)
    session.commit()

