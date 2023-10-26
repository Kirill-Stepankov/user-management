import pytest
from src.users.schemas import UserAddSchema
from tests.conftest import override_auth_service


@pytest.fixture
def user_add_credentials():
    return UserAddSchema(username="test", hashed_password="testtest")


@pytest.fixture
def jwt_tokens(user):
    auth_service = override_auth_service()
    payload = {"uuid": user.uuid, "username": user.username}
    return auth_service.create_tokens(payload)
