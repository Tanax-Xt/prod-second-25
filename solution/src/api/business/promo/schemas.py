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
from enum import Enum
from typing import List, Optional, Literal

from fastapi import Depends, HTTPException, status
from pydantic import BaseModel, constr, conint, HttpUrl, validator
from pydantic_extra_types.country import CountryAlpha2

from src.api.business.promo.deps import parse_list_query, Country


# class Country(BaseModel):
#     country: CountryAlpha2


# class PromoDescription(BaseModel):
#     description: constr(min_length=10, max_length=300)


# class PromoImageURL(BaseModel):
#     avatar_url: Optional[HttpUrl] = None


class Target(BaseModel):
    age_from: Optional[conint(ge=0, le=100)] = None
    age_until: Optional[conint(ge=0, le=100)] = None
    country: Optional[str] = None
    categories: Optional[List[constr(min_length=2, max_length=20)]] = None

    # @validator('categories')
    # def lowercase_categories(cls, v):
    #     if v is not None:
    #         return [category.lower() for category in v]
    #     return v

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

    @validator('age_from', pre=True)
    def test_age(cls, v):
        if type(v) is not int and v is not None:
            raise HTTPException(status.HTTP_400_BAD_REQUEST)
        return v

    @validator('age_until', pre=True)
    def test_age(cls, v):
        if type(v) is not int and v is not None:
            raise HTTPException(status.HTTP_400_BAD_REQUEST)
        return v


class PromoPatch(BaseModel):
    description: Optional[constr(min_length=10, max_length=300)] = None
    image_url: Optional[HttpUrl] = None
    target: Optional[Target] = None
    max_count: Optional[conint(ge=0, le=100000000)] = None
    active_from: Optional[datetime.date] = None
    active_until: Optional[datetime.date] = None


class PromoEnum(str, Enum):
    common = "COMMON"
    unique = "UNIQUE"


class PromoCreate(BaseModel):
    description: constr(min_length=10, max_length=300)
    target: Target
    image_url: Optional[HttpUrl] = None
    max_count: Optional[conint(ge=0, le=100000000)]
    active_from: Optional[datetime.date] = None
    active_until: Optional[datetime.date] = None
    mode: PromoEnum
    promo_common: Optional[constr(min_length=5, max_length=30)] = None
    promo_unique: Optional[List[constr(min_length=3, max_length=30)]] = None


class PromoResponse(PromoCreate):
    promo_id: constr(min_length=1, max_length=50)
    company_id: constr(min_length=1, max_length=50)
    company_name: constr(max_length=100)
    like_count: conint(ge=0)
    used_count: conint(ge=0)
    active: bool


class PromosListSearchParams(BaseModel):
    limit: Optional[conint(ge=0)] = 10
    offset: Optional[conint(ge=0)] = None
    sort_by: Optional[Literal["active_from", "active_until"]] = None
    country: Optional[List[CountryAlpha2]] = Depends(parse_list_query)

    @validator('country')
    def lowercase_country(cls, v):
        if v is not None:
            return [category.lower() for category in v]
        return v
