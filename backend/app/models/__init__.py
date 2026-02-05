from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import models so Alembic can detect them
from app.models.provider import (  # noqa: E402, F401
    CostRecord,
    Provider,
    ProviderStatus,
    ProviderType,
)
from app.models.user import UserProfile  # noqa: E402, F401
