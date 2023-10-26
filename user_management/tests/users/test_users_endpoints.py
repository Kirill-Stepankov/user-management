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
    jwt_tokens,
):
    print(jwt_tokens.get("access_token"))
    response = await ac.get(
        "/user/me", headers={"token": jwt_tokens.get("access_token")}
    )
    assert response.status_code == 200
