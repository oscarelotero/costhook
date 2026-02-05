import uuid
from datetime import datetime

from pydantic import BaseModel


class UserProfileBase(BaseModel):
    display_name: str | None = None
    timezone: str = "UTC"


class UserProfileCreate(UserProfileBase):
    auth_user_id: uuid.UUID


class UserProfileUpdate(BaseModel):
    display_name: str | None = None
    timezone: str | None = None


class UserProfileResponse(UserProfileBase):
    id: uuid.UUID
    auth_user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
