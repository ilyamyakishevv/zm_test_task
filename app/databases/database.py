from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from configs.config import db_settings

SQLALCHEMY_DATABASE_URL = (
    "postgresql+asyncpg://"
    f"{db_settings.POSTGRES_USER}:"
    f"{db_settings.POSTGRES_PASSWORD}@"
    f"{db_settings.POSTGRES_HOST}:"
    f"{db_settings.POSTGRES_PORT}/"
    f"{db_settings.POSTGRES_DB}"
)

async_engine = create_async_engine(
    url=SQLALCHEMY_DATABASE_URL,
    pool_size=70,
    max_overflow=10,
    echo=True,
    pool_timeout=30,
    pool_recycle=300,
)
async_session = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
        await session.close()