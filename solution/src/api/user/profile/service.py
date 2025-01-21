from src.api.user.auth.schemas import UserTargetSettings
from src.api.user.models import User
from src.api.user.profile.schemas import UserResponse


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
