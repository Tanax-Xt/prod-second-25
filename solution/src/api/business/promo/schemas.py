import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, constr, conint, HttpUrl
from pydantic_extra_types.country import CountryAlpha2


class Country(BaseModel):
    country: CountryAlpha2


class PromoDescription(BaseModel):
    description: constr(min_length=10, max_length=300)


class PromoImageURL(BaseModel):
    image_url: HttpUrl


class Target(BaseModel):
    age_from: conint(ge=0, le=100)
    age_until: conint(ge=0, le=100)
    country: Country
    categories: List[constr(min_length=2, max_length=20)]


class PromoPatch(BaseModel):
    description: PromoDescription
    image_url: PromoImageURL
    target: Target
    max_count: Optional[conint(ge=0, le=100000000)]
    active_from: datetime.date
    active_until: datetime.date


class PromoEnum(str, Enum):
    common = "COMMON"
    unique = "UNIQUE"


class PromoCreate(PromoPatch):
    mode: PromoEnum
    promo_common: Optional[constr(min_length=5, max_length=30)]
    promo_unique: Optional[List[constr(min_length=3, max_length=30)]]
