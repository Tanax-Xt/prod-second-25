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

from fastapi import HTTPException, status
from pydantic import constr, HttpUrl, BaseModel, validator
from pydantic_extra_types.country import CountryAlpha2

from src.api.business.promo.deps import Country
from src.api.schemas import Email, Password, Age


class UserTargetSettings(Age, BaseModel):
    country: CountryAlpha2

    @validator('country')
    def lowercase_country(cls, v):
        if v is not None:
            try:
                x = Country(country=v).country
                return v
            except Exception:
                raise HTTPException(status.HTTP_400_BAD_REQUEST)
        else:
            return None


class UserLogin(Email, Password):
    pass


class UserCreate(UserLogin):
    name: constr(min_length=1, max_length=100)
    surname: constr(min_length=1, max_length=120)
    avatar_url: Optional[HttpUrl] = None
    other: UserTargetSettings
