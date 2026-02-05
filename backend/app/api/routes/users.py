from fastapi import APIRouter

from app.api.deps import CurrentUserProfile, SessionDep
from app.crud import user as user_crud
from app.schemas.user import UserProfileResponse, UserProfileUpdate

router = APIRouter()


@router.get("/me", response_model=UserProfileResponse)
async def get_current_user_profile(user_profile: CurrentUserProfile):
    """Get the current user's profile."""
    return user_profile


@router.patch("/me", response_model=UserProfileResponse)
async def update_current_user_profile(
    db: SessionDep,
    user_profile: CurrentUserProfile,
    profile_in: UserProfileUpdate,
):
    """Update the current user's profile."""
    return await user_crud.update(db, user_profile, profile_in)
