"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "fusion" by Rapid Integration (https://github.com/rapid-integration).
Available at: https://github.com/rapid-integration/fusion

This code may be based on "api" by Quotepedia (https://github.com/quotepedia).
Available at: https://github.com/quotepedia/api

Modifications made by Danila Sedelnikov on January 2025.
"""

import uuid

import jwt
from fastapi import status, HTTPException
from sqlalchemy.sql import exists

from src.api.business.auth.schemas import BusinessCreate
from src.api.business.models import Business
from src.api.schemas import JWT
from src.api.service import get_secret
from src.api.service import set_secret
from src.config import settings
from src.db.deps import Session
from src.security import get_password_hash


def get_business_by_email(session: Session, email: str) -> Business | None:
    return session.query(Business).filter(Business.email == email).first()


def is_business_email_registered(session: Session, email: str, ) -> bool:
    return session.query(exists().where(Business.email == email)).scalar()


def create_business(session: Session, schema: BusinessCreate) -> Business:
    business = Business(
        email=schema.email,
        password=get_password_hash(schema.password),
        name=schema.name
    )

    session.add(business)
    session.commit()
    session.refresh(business)

    return business


def update_secret(id: str) -> str:
    secret = uuid.uuid4().hex
    set_secret(id, secret, settings.BUSINESS_SECRET_PREFIX)
    return secret


def get_business_by_token(token: str, session: Session) -> Business:
    raw_token = token.split(" ")[1]
    try:
        unverified_data = jwt.decode(raw_token, options={"verify_signature": False})
        sub = unverified_data.get("sub")
        if not sub:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Email not found in token")

        secret = get_secret(sub, settings.BUSINESS_SECRET_PREFIX)

        data = JWT(**jwt.decode(raw_token, secret, algorithms=[settings.JWT_ALGORITHM]))
    except Exception as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Failed to verify credentials")

    business = session.get(Business, data.sub)
    if not business:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User not found")
    return business
