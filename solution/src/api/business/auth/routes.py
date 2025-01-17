from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["business-auth"])


@router.get("/sing-up")
def sing_up():
    pass
