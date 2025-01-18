from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

__oauth2_bearer = OAuth2PasswordBearer("api/business/auth/sign-in")

PasswordBearer = Annotated[str, Depends(__oauth2_bearer)]
PasswordForm = Annotated[OAuth2PasswordRequestForm, Depends()]
