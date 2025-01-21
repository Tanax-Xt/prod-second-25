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

from pydantic import constr, HttpUrl, BaseModel, conint
from pydantic_extra_types.country import CountryAlpha2

from src.api.schemas import Email, Password


class UserTargetSettings(BaseModel):
    age: conint(ge=0, le=100)
    country: CountryAlpha2


class UserLogin(Email, Password):
    pass


class UserCreate(UserLogin):
    name: constr(min_length=1, max_length=100)
    surname: constr(min_length=1, max_length=120)
    image_url: Optional[HttpUrl] = None
    other: UserTargetSettings
