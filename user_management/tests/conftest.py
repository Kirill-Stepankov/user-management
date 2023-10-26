import asyncio
from typing import AsyncGenerator

import pytest
from fastapi import Header
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from src.abstract import authenticate_stub
from src.auth.exceptions import TokenIsBlacklistedException
from src.auth.service import AbstractAuthService, AuthService
from src.auth.utils import decode_token
from src.config import get_settings
from src.database import Base, async_session_maker
from src.main import app
from src.repository import RedisRepository, S3_repository
from src.users.exceptions import UserInvalidCredentialsException
from src.users.models import Group, User
from src.users.repository import UserRepository
from src.users.service import AbstractUserService, UserService

pytest_plugins = ["users.user_fixtures"]

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


async def override_authenticate(token: str = Header()) -> User:
    auth_serv = override_auth_service()
    user_serv = override_user_service()
    is_blacklisted = await auth_serv.token_is_blacklisted(token)
    if is_blacklisted:
        raise TokenIsBlacklistedException
    payload = decode_token(token)
    uuid = payload.get("uuid")

    is_access = payload.get("is_access")
    if is_access is None:
        raise UserInvalidCredentialsException

    user = await user_serv.get_user(uuid=uuid)
    if user is None:
        raise UserInvalidCredentialsException

    return user


app.dependency_overrides[AbstractUserService] = override_user_service
app.dependency_overrides[AbstractAuthService] = override_auth_service
app.dependency_overrides[authenticate_stub] = override_authenticate


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


@pytest.fixture
async def user(user_add_credentials):
    user_service = override_user_service()
    return await user_service.add_user(user_add_credentials)
