import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from src.auth.service import AbstractAuthService, AuthService
from src.config import get_settings
from src.database import Base, async_session_maker
from src.main import app
from src.repository import RedisRepository, S3_repository
from src.users.models import Group, User
from src.users.repository import UserRepository
from src.users.service import AbstractUserService, UserService

settings = get_settings()

DATABASE_URL_TEST = f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host_test}:{settings.postgres_port}/{settings.postgres_db_test}"

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)
Base.metadata.bind = engine_test


def override_user_service():
    return UserService(UserRepository(async_session_maker), S3_repository)


def override_auth_service():
    return AuthService(UserRepository(async_session_maker), RedisRepository)


app.dependency_overrides[AbstractUserService] = override_user_service
app.dependency_overrides[AbstractAuthService] = override_auth_service


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://") as ac:
        yield ac
