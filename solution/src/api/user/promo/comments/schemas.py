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

from pydantic import BaseModel, constr, HttpUrl, conint


class CommentsToUserSearchParams(BaseModel):
    limit: Optional[conint(ge=0, strict=True)] = 10
    offset: Optional[conint(ge=0, strict=True)] = None


class Author(BaseModel):
    name: constr(min_length=1, max_length=100)
    surname: constr(min_length=1, max_length=120)
    avatar_url: Optional[HttpUrl] = None


class CommentText(BaseModel):
    text: constr(min_length=10, max_length=1000)


class CommentResponse(CommentText):
    id: constr(min_length=1, max_length=50)
    date: constr()
    author: Author
