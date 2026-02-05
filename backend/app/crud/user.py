import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import UserProfile
from app.schemas.user import UserProfileCreate, UserProfileUpdate


async def get_by_auth_user_id(db: AsyncSession, auth_user_id: uuid.UUID) -> UserProfile | None:
    stmt = select(UserProfile).where(UserProfile.auth_user_id == auth_user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create(db: AsyncSession, profile_in: UserProfileCreate) -> UserProfile:
    profile = UserProfile(**profile_in.model_dump())
    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    return profile


async def update(
    db: AsyncSession, profile: UserProfile, profile_in: UserProfileUpdate
) -> UserProfile:
    update_data = profile_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)
    await db.commit()
    await db.refresh(profile)
    return profile


async def get_or_create(db: AsyncSession, auth_user_id: uuid.UUID) -> UserProfile:
    """Get existing profile or create a new one for the auth user."""
    profile = await get_by_auth_user_id(db, auth_user_id)
    if not profile:
        profile = await create(db, UserProfileCreate(auth_user_id=auth_user_id))
    return profile
