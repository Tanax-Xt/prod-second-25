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

from pydantic import BaseModel, constr, conint, validator


class PromoToUserSearchParams(BaseModel):
    limit: Optional[conint(ge=0)] = 10
    offset: Optional[conint(ge=0)] = None
    active: Optional[bool] = True

    category: Optional[constr(min_length=2, max_length=20)] = None

    @validator('category')
    def lowercase_categories(cls, v):
        return v.lower() if v is not None else None
