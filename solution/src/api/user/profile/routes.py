from fastapi import APIRouter, status, HTTPException, Header

from src.api.user.auth.service import get_user_by_token
from src.api.user.profile.schemas import UserResponse
from src.api.user.profile.service import user_to_response
from src.db.deps import Session

profile_router = APIRouter(prefix="/profile", tags=["user-profile"])


@profile_router.get("", status_code=status.HTTP_200_OK, response_model=UserResponse,
                    response_model_exclude_none=True)
def get_profile(Authorization: str = Header(), session: Session = Session) -> UserResponse:
    if not Authorization or not Authorization.startswith("Bearer "):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or missing Authorization header")

    user = get_user_by_token(Authorization, session)

    return user_to_response(user)


@profile_router.patch("")
def patch_profile():
    pass
