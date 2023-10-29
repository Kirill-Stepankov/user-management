import pytest
from httpx import AsyncClient
from src.users.permissions import IsAdmin, IsModerator, IsUsersModerator


@pytest.fixture
def is_admin_mock(mocker):
    mock = mocker.patch.object(IsAdmin, "has_permission")
    return mock


@pytest.fixture
def is_users_moderator_mock(mocker):
    mock = mocker.patch.object(IsUsersModerator, "has_permission")
    return mock


@pytest.fixture
def is_moderator_mock(mocker):
    mock = mocker.patch.object(IsModerator, "has_permission")
    return mock


@pytest.mark.parametrize(
    "is_admin, is_users_moderator, expected_status",
    [
        (True, False, 200),
        (False, True, 200),
        (True, True, 200),
        (False, False, 403),
    ],
)
async def test_get_user(
    is_admin,
    is_users_moderator,
    expected_status,
    ac: AsyncClient,
    jwt_token: dict,
    is_admin_mock,
    is_users_moderator_mock,
    user,
):
    is_admin_mock.return_value = is_admin
    is_users_moderator_mock.return_value = is_users_moderator

    response = await ac.get(
        f"/user/{user.uuid}", headers={"token": jwt_token.get("access_token")}
    )

    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "token, expected_status",
    [
        (pytest.lazy_fixture("jwt_token"), 200),
        (pytest.lazy_fixture("invalid_jwt_token"), 401),
    ],
)
async def test_get_me(
    token: dict,
    expected_status: int,
    ac: AsyncClient,
):
    response = await ac.get("/user/me", headers={"token": token.get("access_token")})
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "token, expected_status",
    [
        (pytest.lazy_fixture("jwt_token"), 200),
        (pytest.lazy_fixture("invalid_jwt_token"), 401),
    ],
)
async def test_delete_me(
    token: dict,
    expected_status: int,
    ac: AsyncClient,
):
    response = await ac.delete("user/me", headers={"token": token.get("access_token")})
    assert response.status_code == expected_status


async def test_patch_me(
    ac: AsyncClient,
    jwt_token: dict,
):
    pass


@pytest.mark.parametrize(
    "is_admin, is_moderator, expected_status",
    [
        (True, False, 200),
        (False, True, 200),
        (True, True, 200),
        (False, False, 403),
    ],
)
async def test_get_users(
    is_admin,
    is_moderator,
    expected_status,
    ac: AsyncClient,
    jwt_token: dict,
    is_admin_mock,
    is_moderator_mock,
):
    is_admin_mock.return_value = is_admin
    is_moderator_mock.return_value = is_moderator

    params = {
        "page": 1,
        "limit": 2,
        "filter_by_name": "test",
        "sort_by": "username",
        "order_by": "desc",
    }

    response = await ac.get(
        "user/", params=params, headers={"token": jwt_token.get("access_token")}
    )

    assert response.status_code == expected_status
