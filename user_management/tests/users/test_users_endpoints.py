import pytest
from httpx import AsyncClient
from sqlalchemy import insert, select
from src.users.models import Group
from tests.conftest import async_session_maker


async def test_add_role():
    async with async_session_maker() as session:
        stmt = insert(Group).values(name="wow")
        await session.execute(stmt)
        await session.commit()

        query = select(Group)
        result = await session.execute(query)
        assert result.all()[0][0].name == "wow"


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


# TODO
# подумать о всевозможных случаях вызова эндпоинтов:
#   валидный токен, не валидный(несколько видов)
# удалить не существующего и тд


async def test_get_user(
    ac: AsyncClient,
    jwt_token: dict,
):
    pass
