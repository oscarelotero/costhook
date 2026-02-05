import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.provider import CostRecord, Provider
from app.schemas.cost import CostFilters, CostRecordCreate


async def get_by_user(
    db: AsyncSession,
    user_id: uuid.UUID,
    filters: CostFilters | None = None,
) -> list[CostRecord]:
    stmt = (
        select(CostRecord)
        .join(Provider)
        .where(Provider.user_id == user_id)
        .order_by(CostRecord.period_start.desc())
    )

    if filters:
        if filters.provider_id:
            stmt = stmt.where(CostRecord.provider_id == filters.provider_id)
        if filters.provider_type:
            stmt = stmt.where(Provider.type == filters.provider_type)
        if filters.start_date:
            stmt = stmt.where(CostRecord.period_start >= filters.start_date)
        if filters.end_date:
            stmt = stmt.where(CostRecord.period_end <= filters.end_date)

    result = await db.execute(stmt)
    return list(result.scalars().all())


async def create(db: AsyncSession, cost_in: CostRecordCreate) -> CostRecord:
    cost = CostRecord(**cost_in.model_dump())
    db.add(cost)
    await db.commit()
    await db.refresh(cost)
    return cost


async def create_many(db: AsyncSession, costs: list[CostRecordCreate]) -> list[CostRecord]:
    records = [CostRecord(**cost.model_dump()) for cost in costs]
    db.add_all(records)
    await db.commit()
    for record in records:
        await db.refresh(record)
    return records
