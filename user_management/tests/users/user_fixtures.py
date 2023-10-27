import pytest
from src.auth.dependencies import auth_service
from src.users.schemas import UserAddSchema
from tests.conftest import async_session_maker


@pytest.fixture
def user_add_credentials():
    return UserAddSchema(username="test", hashed_password="testtest")


@pytest.fixture
def jwt_token(user):
    auth_serv = auth_service(async_session_maker)
    payload = {"uuid": user.uuid, "username": user.username}
    return auth_serv.create_tokens(payload)


@pytest.fixture
def invalid_jwt_token():
    return {"access_token": "invalid", "refresh_token": "invalid"}
