from fastapi import APIRouter, status, HTTPException

from src.api.user.auth.schemas import UserCreate, UserLogin
from src.api.user.auth.service import update_secret, is_user_email_registered, create_user, get_user_by_email
from src.db.deps import Session
from src.security import create_access_token, is_valid_password

auth_router = APIRouter(prefix="/auth", tags=["user-auth"])


@auth_router.post("/sign-up", status_code=status.HTTP_200_OK)
async def sing_up(user_create_model: UserCreate, session: Session):
    if is_user_email_registered(session, user_create_model.email):
        raise HTTPException(status.HTTP_409_CONFLICT, "Email already registered.")

    user = create_user(session, user_create_model)
    secret = update_secret(user.id.hex)
    return create_access_token(user.id.hex, secret)


@auth_router.post("/sign-in", status_code=status.HTTP_200_OK)
async def sing_in(user_create_model: UserLogin, session: Session):
    user = get_user_by_email(session, user_create_model.email)

    if not user or not is_valid_password(user_create_model.password, user.password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Incorrect email or password.")

    secret = update_secret(user.id.hex)
    return create_access_token(user.id.hex, secret)
