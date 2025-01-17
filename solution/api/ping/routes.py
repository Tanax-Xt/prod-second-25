from fastapi import APIRouter, HTTPException, status


router = APIRouter(prefix="/ping", tags=["ping"])


@router.get("", status_code=status.HTTP_200_OK)
def ping():
    return {"status": "proooooood"}
