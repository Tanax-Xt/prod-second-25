from typing import Optional

from pydantic import constr, HttpUrl

from src.api.schemas import Email
from src.api.user.auth.schemas import UserTargetSettings


class UserResponse(Email):
    name: constr(min_length=1, max_length=100)
    surname: constr(min_length=1, max_length=120)
    image_url: Optional[HttpUrl] = None
    other: UserTargetSettings
