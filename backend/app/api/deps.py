import uuid
from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import AsyncSessionLocal
from app.core.security import verify_token
from app.crud import user as user_crud
from app.models.user import UserProfile

security = HTTPBearer()


async def get_db() -> AsyncGenerator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        yield session


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> dict:
    """Get the current authenticated user from the JWT token."""
    payload = verify_token(credentials.credentials)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )
    return {
        "id": user_id,
        "email": payload.get("email"),
        "role": payload.get("role"),
    }


async def get_current_user_profile(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
) -> UserProfile:
    """Get or create the user profile for the authenticated user."""
    auth_user_id = uuid.UUID(current_user["id"])
    return await user_crud.get_or_create(db, auth_user_id)


SessionDep = Annotated[AsyncSession, Depends(get_db)]
CurrentUser = Annotated[dict, Depends(get_current_user)]
CurrentUserProfile = Annotated[UserProfile, Depends(get_current_user_profile)]
