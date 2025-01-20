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
