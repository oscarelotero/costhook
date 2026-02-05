import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Query

from app.api.deps import CurrentUserProfile, SessionDep
from app.crud import cost as cost_crud
from app.models.provider import ProviderType
from app.schemas.cost import CostFilters, CostRecordResponse

router = APIRouter()


@router.get("", response_model=list[CostRecordResponse])
def list_costs(
    db: SessionDep,
    user_profile: CurrentUserProfile,
    provider_id: Annotated[uuid.UUID | None, Query()] = None,
    provider_type: Annotated[ProviderType | None, Query()] = None,
    start_date: Annotated[datetime | None, Query()] = None,
    end_date: Annotated[datetime | None, Query()] = None,
):
    """List cost records for the current user with optional filters."""
    filters = CostFilters(
        provider_id=provider_id,
        provider_type=provider_type,
        start_date=start_date,
        end_date=end_date,
    )
    return cost_crud.get_by_user(db, user_profile.id, filters)
