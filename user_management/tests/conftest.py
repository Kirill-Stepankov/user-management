import asyncio
from functools import partial
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from src.abstract import authenticate_stub
from src.auth.dependencies import auth_service
from src.auth.service import AbstractAuthService
from src.config import get_settings
from src.database import Base
from src.di import AuthenticatePartial
from src.main import create_app
from src.users.dependencies import user_service
from src.users.models import Group, User
from src.users.service import AbstractUserService

pytest_plugins = ["users.user_fixtures"]

settings = get_settings()

DATABASE_URL_TEST = f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host_test}:{settings.postgres_port}/{settings.postgres_db_test}"

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False, autoflush=False
)

Base.metadata.bind = engine_test


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
    app = create_app()

    app.dependency_overrides[AbstractUserService] = partial(
        user_service, async_session_maker
    )
    app.dependency_overrides[AbstractAuthService] = partial(
        auth_service, async_session_maker
    )
    app.dependency_overrides[authenticate_stub] = AuthenticatePartial(
        user_service(async_session_maker), auth_service(async_session_maker)
    )

    async with AsyncClient(app=app, base_url="http://") as ac:
        yield ac


@pytest.fixture
async def user_serv():
    return user_service(async_session_maker)


@pytest.fixture
async def auth_serv():
    return auth_service(async_session_maker)


@pytest.fixture
async def user(user_add_credentials, user_serv):
    user = await user_serv.add_user(user_add_credentials)
    yield user
    await user_serv.delete_user(user.uuid)
