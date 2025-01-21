from typing import Optional

from pydantic import constr, HttpUrl, BaseModel, validator

from src.api.schemas import Email
from src.api.user.auth.schemas import UserTargetSettings


class UserResponse(Email):
    name: constr(min_length=1, max_length=100)
    surname: constr(min_length=1, max_length=120)
    image_url: Optional[HttpUrl] = None
    other: UserTargetSettings


class UserPatch(BaseModel):
    name: Optional[constr(min_length=1, max_length=100)] = None
    surname: Optional[constr(min_length=1, max_length=120)] = None
    image_url: Optional[HttpUrl] = None
    password: Optional[constr(min_length=8, max_length=60)] = None

    @validator('password')
    def validate_password(cls, v):
        if not any(c.islower() for c in v):
            raise ValueError()
        if not any(c.isupper() for c in v):
            raise ValueError()
        if not any(c.isdigit() for c in v):
            raise ValueError()
        if not any(c in '@$!%*?&' for c in v):
            raise ValueError()
        return v
