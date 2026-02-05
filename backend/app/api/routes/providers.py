import uuid

from fastapi import APIRouter, HTTPException, status

from app.api.deps import CurrentUserProfile, SessionDep
from app.crud import provider as provider_crud
from app.schemas.provider import ProviderCreate, ProviderResponse, ProviderUpdate

router = APIRouter()


@router.get("", response_model=list[ProviderResponse])
def list_providers(
    db: SessionDep,
    user_profile: CurrentUserProfile,
):
    """List all providers for the current user."""
    return provider_crud.get_by_user(db, user_profile.id)


@router.post("", response_model=ProviderResponse, status_code=status.HTTP_201_CREATED)
def create_provider(
    db: SessionDep,
    user_profile: CurrentUserProfile,
    provider_in: ProviderCreate,
):
    """Create a new provider connection."""
    return provider_crud.create(db, user_profile.id, provider_in)


@router.get("/{provider_id}", response_model=ProviderResponse)
def get_provider(
    db: SessionDep,
    user_profile: CurrentUserProfile,
    provider_id: uuid.UUID,
):
    """Get a specific provider by ID."""
    provider = provider_crud.get(db, provider_id)
    if not provider or provider.user_id != user_profile.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Provider not found",
        )
    return provider


@router.patch("/{provider_id}", response_model=ProviderResponse)
def update_provider(
    db: SessionDep,
    user_profile: CurrentUserProfile,
    provider_id: uuid.UUID,
    provider_in: ProviderUpdate,
):
    """Update a provider."""
    provider = provider_crud.get(db, provider_id)
    if not provider or provider.user_id != user_profile.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Provider not found",
        )
    return provider_crud.update(db, provider, provider_in)


@router.delete("/{provider_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_provider(
    db: SessionDep,
    user_profile: CurrentUserProfile,
    provider_id: uuid.UUID,
):
    """Delete a provider and all its cost records."""
    provider = provider_crud.get(db, provider_id)
    if not provider or provider.user_id != user_profile.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Provider not found",
        )
    provider_crud.delete(db, provider)
