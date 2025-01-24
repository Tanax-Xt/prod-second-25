"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "fusion" by Rapid Integration (https://github.com/rapid-integration).
Available at: https://github.com/rapid-integration/fusion

This code may be based on "api" by Quotepedia (https://github.com/quotepedia).
Available at: https://github.com/quotepedia/api

Modifications made by Danila Sedelnikov on January 2025.
"""

from src.api.user.auth.schemas import UserTargetSettings
from src.api.user.models import User
from src.api.user.profile.schemas import UserResponse, UserPatch
from src.db.deps import Session
from src.security import get_password_hash


def get_user_target_response(user: User) -> UserTargetSettings:
    return UserTargetSettings(
        age=user.age,
        country=user.country
    )


def user_to_response(user: User) -> UserResponse:
    return UserResponse(
        name=user.name,
        surname=user.surname,
        email=user.email,
        image_url=user.avatar_url,
        other=get_user_target_response(user)
    )


def update_user(user: User, schema: UserPatch, session: Session) -> User:
    for param in schema.dict(exclude_unset=True):
        if param == "password":
            setattr(user, param, get_password_hash(getattr(schema, param)))
        else:
            setattr(user, param, getattr(schema, param))

    session.commit()
    session.refresh(user)
    return user
