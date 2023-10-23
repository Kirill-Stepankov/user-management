def test_a():
    assert 1 == 1


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
