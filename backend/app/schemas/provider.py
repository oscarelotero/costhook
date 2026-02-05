import uuid
from datetime import datetime

from pydantic import BaseModel

from app.models.provider import ProviderStatus, ProviderType


class ProviderBase(BaseModel):
    name: str
    type: ProviderType


class ProviderCreate(ProviderBase):
    credentials: dict


class ProviderUpdate(BaseModel):
    name: str | None = None
    credentials: dict | None = None


class ProviderResponse(ProviderBase):
    id: uuid.UUID
    user_id: uuid.UUID
    status: ProviderStatus
    last_sync_at: datetime | None
    last_error: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
