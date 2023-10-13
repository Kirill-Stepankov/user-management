from abc import ABC, abstractmethod

from sqlalchemy import insert, select

from .database import async_session_maker


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one():
        raise NotImplementedError

    @abstractmethod
    async def find():
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def add_one(self, data: dict) -> int:
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model.uuid)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def find(self, **filters):
        async with async_session_maker() as session:
            stmt = select(self.model).filter_by(**filters)
            res = await session.execute(stmt)
            return res.all()
