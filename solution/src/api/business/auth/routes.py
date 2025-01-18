import uuid

from fastapi import APIRouter, status, HTTPException

from src.api.business.auth.schemas import BusinessCreate
from src.api.business.auth.service import is_business_email_registered, create_business
from src.api.service import set_secret
from src.db.deps import Session
from src.security import create_access_token

auth_router = APIRouter(prefix="/auth", tags=["business-auth"])


@auth_router.post("/sing-up", status_code=status.HTTP_200_OK)
async def sing_up(business_create_model: BusinessCreate, session: Session):
    if is_business_email_registered(session, business_create_model.email, business_create_model.name):
        raise HTTPException(status.HTTP_409_CONFLICT, "Email already registered.")

    business = create_business(session, business_create_model)
    secret = uuid.uuid4().hex
    set_secret(business.id.hex, secret, 'secret')
    return create_access_token(business.id.hex, secret)
