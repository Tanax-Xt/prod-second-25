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

from pydantic import BaseModel, constr, conint, validator, HttpUrl


class PromoToUserSearchParams(BaseModel):
    limit: Optional[conint(ge=0)] = 10
    offset: Optional[conint(ge=0)] = None
    active: Optional[bool] = True

    category: Optional[constr(min_length=2, max_length=20)] = None

    @validator('category')
    def lowercase_categories(cls, v):
        return v.lower() if v is not None else None


class PromoForUser(BaseModel):
    promo_id: constr(min_length=1, max_length=50)
    company_id: constr(min_length=1, max_length=50)
    company_name: constr(max_length=100)
    description: constr(min_length=10, max_length=300)
    image_url: Optional[HttpUrl] = None
    active: bool
    is_activated_by_user: bool
    like_count: conint(ge=0)
    is_liked_by_user: bool
    comment_count: conint(ge=0)