import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.crypto import encrypt_credentials
from app.models.provider import Provider
from app.schemas.provider import ProviderCreate, ProviderUpdate


def get(db: Session, provider_id: uuid.UUID) -> Provider | None:
    return db.get(Provider, provider_id)


def get_by_user(db: Session, user_id: uuid.UUID) -> list[Provider]:
    stmt = select(Provider).where(Provider.user_id == user_id).order_by(Provider.created_at.desc())
    return list(db.execute(stmt).scalars().all())


def create(db: Session, user_id: uuid.UUID, provider_in: ProviderCreate) -> Provider:
    provider = Provider(
        user_id=user_id,
        name=provider_in.name,
        type=provider_in.type,
        credentials_encrypted=encrypt_credentials(provider_in.credentials),
    )
    db.add(provider)
    db.commit()
    db.refresh(provider)
    return provider


def update(db: Session, provider: Provider, provider_in: ProviderUpdate) -> Provider:
    update_data = provider_in.model_dump(exclude_unset=True)

    if "credentials" in update_data:
        credentials = update_data.pop("credentials")
        if credentials is not None:
            provider.credentials_encrypted = encrypt_credentials(credentials)

    for field, value in update_data.items():
        setattr(provider, field, value)

    db.commit()
    db.refresh(provider)
    return provider


def delete(db: Session, provider: Provider) -> None:
    db.delete(provider)
    db.commit()
