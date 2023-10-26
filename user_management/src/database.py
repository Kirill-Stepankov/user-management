from contextlib import asynccontextmanager
from typing import AsyncGenerator, AsyncIterator

import aioboto3
from redis.asyncio import ConnectionPool, Redis
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .config import get_settings

settings = get_settings()


def create_session_maker():
    DATABASE_URL = f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"

    engine = create_async_engine(DATABASE_URL)
    return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


pool = ConnectionPool.from_url("redis://redis", encoding="utf-8", decode_responses=True)


class Base(DeclarativeBase):
    pass


@asynccontextmanager
async def init_redis_pool() -> AsyncIterator[Redis]:
    client = Redis.from_pool(pool)
    yield client
    await client.close()


session = aioboto3.Session()


@asynccontextmanager
async def aws_client(service):
    async with session.client(
        service,
        endpoint_url=settings.localstack_endpoint_url,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
        region_name="us-east-1",
    ) as s3:
        yield s3
