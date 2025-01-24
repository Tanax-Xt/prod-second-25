"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "fusion" by Rapid Integration (https://github.com/rapid-integration).
Available at: https://github.com/rapid-integration/fusion

This code may be based on "api" by Quotepedia (https://github.com/quotepedia).
Available at: https://github.com/quotepedia/api

Modifications made by Danila Sedelnikov on January 2025.
"""

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
    avatar_url: Optional[HttpUrl] = None
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
