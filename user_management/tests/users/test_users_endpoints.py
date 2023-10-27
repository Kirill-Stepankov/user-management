import pytest
from httpx import AsyncClient


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


async def test_get_user(
    ac: AsyncClient,
    jwt_token: dict,
):
    pass
