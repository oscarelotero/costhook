from fastapi import APIRouter

from app.api.deps import CurrentUser

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "healthy"}


@router.get("/health/protected")
def protected_health_check(current_user: CurrentUser):
    return {"status": "healthy", "user_id": current_user["id"]}
