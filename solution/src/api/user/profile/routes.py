from fastapi import APIRouter, status, HTTPException, Header

from src.api.user.auth.service import get_user_by_token
from src.api.user.profile.schemas import UserResponse, UserPatch
from src.api.user.profile.service import user_to_response, update_user

"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "fusion" by Rapid Integration (https://github.com/rapid-integration).
Available at: https://github.com/rapid-integration/fusion

This code may be based on "api" by Quotepedia (https://github.com/quotepedia).
Available at: https://github.com/quotepedia/api

Modifications made by Danila Sedelnikov on January 2025.
"""

from src.db.deps import Session

profile_router = APIRouter(prefix="/profile", tags=["user-profile"])


@profile_router.get("", status_code=status.HTTP_200_OK, response_model=UserResponse,
                    response_model_exclude_none=True)
def get_profile(Authorization: str = Header(), session: Session = Session) -> UserResponse:
    if not Authorization or not Authorization.startswith("Bearer "):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or missing Authorization header")

    user = get_user_by_token(Authorization, session)

    return user_to_response(user)


@profile_router.patch("", status_code=status.HTTP_200_OK, response_model=UserResponse,
                      response_model_exclude_none=True)
def patch_profile(user_patch: UserPatch, Authorization: str = Header(), session: Session = Session) -> UserResponse:
    if not Authorization or not Authorization.startswith("Bearer "):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or missing Authorization header")

    user = get_user_by_token(Authorization, session)
    user = update_user(user, user_patch, session)

    return user_to_response(user)
