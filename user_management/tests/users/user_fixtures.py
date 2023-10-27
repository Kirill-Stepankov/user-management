import pytest
from src.auth.dependencies import auth_service
from src.users.schemas import UserAddSchema
from tests.conftest import async_session_maker


@pytest.fixture
def user_add_credentials():
    return UserAddSchema(username="test", hashed_password="testtest")


@pytest.fixture
def jwt_tokens(user):
    auth_serv = auth_service(async_session_maker)
    payload = {"uuid": user.uuid, "username": user.username}
    return auth_serv.create_tokens(payload)
