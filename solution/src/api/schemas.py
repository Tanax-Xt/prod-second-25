from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, constr, validator


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
    access_token: str
    token_type: str = "bearer"
    expires_at: datetime


class JWT(BaseModel):
    exp: datetime | None = None
    sub: int | str | None = None
