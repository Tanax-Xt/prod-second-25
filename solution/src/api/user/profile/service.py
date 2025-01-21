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
        image_url=user.image_url,
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
