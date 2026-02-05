import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import UserProfile
from app.schemas.user import UserProfileCreate, UserProfileUpdate


def get_by_auth_user_id(db: Session, auth_user_id: uuid.UUID) -> UserProfile | None:
    stmt = select(UserProfile).where(UserProfile.auth_user_id == auth_user_id)
    return db.execute(stmt).scalar_one_or_none()


def create(db: Session, profile_in: UserProfileCreate) -> UserProfile:
    profile = UserProfile(**profile_in.model_dump())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def update(db: Session, profile: UserProfile, profile_in: UserProfileUpdate) -> UserProfile:
    update_data = profile_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)
    db.commit()
    db.refresh(profile)
    return profile


def get_or_create(db: Session, auth_user_id: uuid.UUID) -> UserProfile:
    """Get existing profile or create a new one for the auth user."""
    profile = get_by_auth_user_id(db, auth_user_id)
    if not profile:
        profile = create(db, UserProfileCreate(auth_user_id=auth_user_id))
    return profile
