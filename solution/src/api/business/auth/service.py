from sqlalchemy.orm import Session
from sqlalchemy.sql import exists

from src.api.business.auth.schemas import BusinessCreate
from src.api.business.models import Business
from src.security import get_password_hash


# def get_user_by_email(session: Session, email: str) -> User | None:
#     return session.query(User).filter(User.email == email).first()


def is_business_email_registered(session: Session, email: str, name: str) -> bool:
    return session.query(exists().where(((Business.email == email) | (Business.name == name)))).scalar()


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
