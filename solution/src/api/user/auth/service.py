import uuid

import jwt
from fastapi import status, HTTPException
from sqlalchemy.sql import exists

from src.api.business.auth.schemas import BusinessCreate
from src.api.business.models import Business
from src.api.schemas import JWT
from src.api.service import get_secret
from src.api.service import set_secret
from src.api.user.models import User
from src.config import settings
from src.db.deps import Session
from src.security import get_password_hash


def get_user_by_email(session: Session, email: str) -> User | None:
    return session.query(Business).filter(Business.email == email).first()


# def is_business_email_registered(session: Session, email: str, name: str) -> bool:
#     return session.query(exists().where(((Business.email == email) | (Business.name == name)))).scalar()


# def create_business(session: Session, schema: BusinessCreate) -> Business:
#     business = Business(
#         email=schema.email,
#         password=get_password_hash(schema.password),
#         name=schema.name
#     )
#
#     session.add(business)
#     session.commit()
#     session.refresh(business)
#
#     return business


def update_secret(id: str) -> str:
    secret = uuid.uuid4().hex
    set_secret(id, secret, settings.USER_SECRET_PREFIX)
    return secret


# def get_business_by_token(token: str, session: Session) -> Business:
#     raw_token = token.split(" ")[1]
#     try:
#         unverified_data = jwt.decode(raw_token, options={"verify_signature": False})
#         sub = unverified_data.get("sub")
#         if not sub:
#             raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Email not found in token")
#
#         secret = get_secret(sub, settings.BUSINESS_SECRET_PREFIX)
#
#         data = JWT(**jwt.decode(raw_token, secret, algorithms=[settings.JWT_ALGORITHM]))
#     except Exception as e:
#         raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Failed to verify credentials")
#
#     business = session.get(Business, data.sub)
#     if not business:
#         raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User not found")
#     return business
