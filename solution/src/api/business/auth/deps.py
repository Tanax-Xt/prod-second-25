from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.api.business.models import Business
from src.api.schemas import JWT
from src.api.service import get_secret
from src.config import settings
from src.db.deps import Session

__oauth2_bearer = OAuth2PasswordBearer("api/business/auth/sign-in")

PasswordBearer = Annotated[str, Depends(__oauth2_bearer)]


# PasswordForm = Annotated[OAuth2PasswordRequestForm, Depends()]


def __get_current_business(session: Session, raw: PasswordBearer) -> Business:
    try:
        unverified_data = jwt.decode(raw, options={"verify_signature": False})
        sub = unverified_data.get("sub")
        if not sub:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Email not found in token")
        secret = get_secret(sub, settings.BUSINESS_SECRET_PREFIX)

        data = JWT(**jwt.decode(raw, secret, algorithms=[settings.JWT_ALGORITHM]))
    except Exception:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Failed to verify credentials")

    business = session.get(Business, data.sub)
    if not business:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User not found")
    return business


CurrentBusiness = Annotated[Business, Depends(__get_current_business)]
