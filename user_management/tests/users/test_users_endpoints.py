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


async def test_get_me(
    ac: AsyncClient,
    jwt_tokens: dict,
):
    response = await ac.get(
        "/user/me", headers={"token": jwt_tokens.get("access_token")}
    )
    print(response)
    assert response.status_code == 200


async def test_delete_me(
    ac: AsyncClient,
    jwt_tokens: dict,
):
    response = await ac.delete(
        "user/me", headers={"token": jwt_tokens.get("access_token")}
    )
    assert response.status_code == 200


async def test_patch_me(
    ac: AsyncClient,
    jwt_tokens: dict,
):
    pass


# TODO
# подумать о всевозможных случаях вызова эндпоинтов:
#   валидный токен, не валидный(несколько видов)
# удалить не существующего и тд


async def test_get_user(
    ac: AsyncClient,
    jwt_tokens: dict,
):
    pass
