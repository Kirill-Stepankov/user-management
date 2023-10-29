import pytest
from httpx import AsyncClient
from src.users.schemas import EmailSchema, ResetPasswordSchema, UserAddSchema


@pytest.fixture
def invalid_user_data():
    return UserAddSchema(username="invalid", hashed_password="invalidd")


@pytest.fixture
def valid_user_data():
    return UserAddSchema(username="test", hashed_password="testtest")


async def test_signup(ac: AsyncClient, user_add_credentials):
    user_add_credentials.username = "testtest"
    response = await ac.post(
        "/auth/signup", data=user_add_credentials.model_dump_json()
    )

    assert response.status_code == 201
    assert response.json().get("username") == user_add_credentials.username


@pytest.mark.parametrize(
    "data, expected_status",
    [
        (pytest.lazy_fixture("invalid_user_data"), 422),
        (pytest.lazy_fixture("valid_user_data"), 200),
    ],
)
async def test_login(
    data,
    expected_status,
    ac: AsyncClient,
    user,
):
    response = await ac.post("/auth/login", data=data.model_dump_json())

    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "token, expected_status",
    [
        (pytest.lazy_fixture("jwt_token"), 201),
        (pytest.lazy_fixture("invalid_jwt_token"), 401),
    ],
)
async def test_change_password(token, expected_status, ac: AsyncClient, user):
    data = ResetPasswordSchema(password="11111111", repeat_password="11111111")

    response = await ac.post(
        "/auth/change-password",
        data=data.model_dump_json(),
        params={"token": token.get("access_token")},
    )

    assert response.status_code == expected_status


async def test_reset_password(
    ac: AsyncClient,
    user,
):
    data = EmailSchema(email="test@mail.com")
    response = await ac.post("/auth/reset-password", data=data.model_dump_json())

    assert response.status_code == 200


@pytest.mark.parametrize(
    "token, expected_status",
    [
        (pytest.lazy_fixture("jwt_token"), 200),
        (pytest.lazy_fixture("invalid_jwt_token"), 401),
    ],
)
async def test_refresh_token(
    token,
    expected_status,
    ac: AsyncClient,
):
    response = await ac.post(
        "/auth/refresh-token", headers={"token": token.get("refresh_token")}
    )

    assert response.status_code == expected_status
