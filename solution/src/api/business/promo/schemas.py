import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, constr, conint, HttpUrl
from pydantic_extra_types.country import CountryAlpha2


class Country(BaseModel):
    country: CountryAlpha2


# class PromoDescription(BaseModel):
#     description: constr(min_length=10, max_length=300)


# class PromoImageURL(BaseModel):
#     image_url: Optional[HttpUrl] = None


class Target(BaseModel):
    age_from: Optional[conint(ge=0, le=100)] = None
    age_until: Optional[conint(ge=0, le=100)] = None
    country: Optional[Country] = None
    categories: Optional[List[constr(max_length=20)]] = None


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
    active_from: datetime.date = None
    active_until: datetime.date = None
    mode: PromoEnum
    promo_common: Optional[constr(min_length=5, max_length=30)] = None
    promo_unique: Optional[List[constr(min_length=3, max_length=30)]] = None
