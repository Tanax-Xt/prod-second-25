"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "fusion" by Rapid Integration (https://github.com/rapid-integration).
Available at: https://github.com/rapid-integration/fusion

This code may be based on "api" by Quotepedia (https://github.com/quotepedia).
Available at: https://github.com/quotepedia/api

Modifications made by Danila Sedelnikov on January 2025.
"""

from datetime import datetime

from fastapi import HTTPException, status
from pydantic import EmailStr, Field
from pydantic import constr, BaseModel, conint, validator


class Age(BaseModel):
    age: conint(ge=0, le=100)

    @validator('age', pre=True)
    def test_age(cls, v):
        if type(v) is not int:
            raise HTTPException(status.HTTP_400_BAD_REQUEST)
        return v


class Email(BaseModel):
    email: EmailStr = Field(min_length=8, max_length=120)


class Password(BaseModel):
    password: constr(
        min_length=8,
        max_length=60,
    )

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


class Token(BaseModel):
    token: str
    token_type: str = "bearer"
    expires_at: datetime


class JWT(BaseModel):
    exp: datetime | None = None
    sub: int | str | None = None
