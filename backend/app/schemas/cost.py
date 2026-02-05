import uuid
from datetime import datetime

from pydantic import BaseModel

from app.models.provider import ProviderType


class CostRecordBase(BaseModel):
    amount: float
    service: str
    period_start: datetime
    period_end: datetime
    metadata_json: str | None = None


class CostRecordCreate(CostRecordBase):
    provider_id: uuid.UUID


class CostRecordResponse(CostRecordBase):
    id: uuid.UUID
    provider_id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}


class CostRecordWithProvider(CostRecordResponse):
    provider_name: str
    provider_type: ProviderType


class CostFilters(BaseModel):
    provider_id: uuid.UUID | None = None
    provider_type: ProviderType | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
