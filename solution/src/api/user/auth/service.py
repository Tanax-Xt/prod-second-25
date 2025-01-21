import uuid

import jwt
from fastapi import status, HTTPException
from sqlalchemy.sql import exists

from src.api.schemas import JWT
from src.api.service import get_secret
from src.api.service import set_secret
from src.api.user.auth.schemas import UserCreate
from src.api.user.models import User
from src.config import settings
from src.db.deps import Session
from src.security import get_password_hash


def get_user_by_email(session: Session, email: str) -> User | None:
    return session.query(User).filter(User.email == email).first()


def is_user_email_registered(session: Session, email: str) -> bool:
    return session.query(exists().where(User.email == email)).scalar()


def create_user(session: Session, schema: UserCreate) -> User:
    user = User(
        email=schema.email,
        password=get_password_hash(schema.password),
        name=schema.name,
        surname=schema.surname,
        image_url=str(schema.image_url) if schema.image_url is not None else None,
        age=schema.other.age,
        country=schema.other.country
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def update_secret(id: str) -> str:
    secret = uuid.uuid4().hex
    set_secret(id, secret, settings.USER_SECRET_PREFIX)
    return secret


def get_user_by_token(token: str, session: Session) -> User:
    raw_token = token.split(" ")[1]
    try:
        unverified_data = jwt.decode(raw_token, options={"verify_signature": False})
        sub = unverified_data.get("sub")
        if not sub:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Email not found in token")

        secret = get_secret(sub, settings.USER_SECRET_PREFIX)

        data = JWT(**jwt.decode(raw_token, secret, algorithms=[settings.JWT_ALGORITHM]))
    except Exception as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Failed to verify credentials")

    user = session.get(User, data.sub)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User not found")
    return user
