from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import settings

# Derive async connection URL from the sync one
async_database_url = settings.DATABASE_URL.replace(
    "postgresql+psycopg://", "postgresql+psycopg_async://"
)

engine = create_async_engine(async_database_url)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
