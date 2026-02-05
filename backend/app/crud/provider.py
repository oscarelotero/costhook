import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.crypto import encrypt_credentials
from app.models.provider import Provider
from app.schemas.provider import ProviderCreate, ProviderUpdate


async def get(db: AsyncSession, provider_id: uuid.UUID) -> Provider | None:
    return await db.get(Provider, provider_id)


async def get_by_user(db: AsyncSession, user_id: uuid.UUID) -> list[Provider]:
    stmt = select(Provider).where(Provider.user_id == user_id).order_by(Provider.created_at.desc())
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def create(db: AsyncSession, user_id: uuid.UUID, provider_in: ProviderCreate) -> Provider:
    provider = Provider(
        user_id=user_id,
        name=provider_in.name,
        type=provider_in.type,
        credentials_encrypted=encrypt_credentials(provider_in.credentials),
    )
    db.add(provider)
    await db.commit()
    await db.refresh(provider)
    return provider


async def update(db: AsyncSession, provider: Provider, provider_in: ProviderUpdate) -> Provider:
    update_data = provider_in.model_dump(exclude_unset=True)

    if "credentials" in update_data:
        credentials = update_data.pop("credentials")
        if credentials is not None:
            provider.credentials_encrypted = encrypt_credentials(credentials)

    for field, value in update_data.items():
        setattr(provider, field, value)

    await db.commit()
    await db.refresh(provider)
    return provider


async def delete(db: AsyncSession, provider: Provider) -> None:
    await db.delete(provider)
    await db.commit()
