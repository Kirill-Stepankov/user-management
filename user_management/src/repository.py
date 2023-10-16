from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import delete, insert, select

from .database import async_session_maker, init_redis_pool


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one():
        raise NotImplementedError

    @abstractmethod
    async def find():
        raise NotImplementedError

    @abstractmethod
    async def get():
        raise NotImplementedError

    @abstractmethod
    async def delete():
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def add_one(self, data: dict) -> str:
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model.uuid)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def find(self, **filters) -> list[model]:
        async with async_session_maker() as session:
            stmt = select(self.model).filter_by(**filters)
            res = await session.scalars(stmt)
            return res.all()

    async def get(self, **filters) -> model:
        async with async_session_maker() as session:
            stmt = select(self.model).filter_by(**filters)
            res = await session.scalars(stmt)
            return res.first()

    async def delete(self, **filters):
        async with async_session_maker() as session:
            stmt = delete(self.model).filter_by(**filters)
            res = await session.execute(stmt)
            await session.commit()


class RedisRepository(AbstractRepository):
    async def add_one(self, key: Any, value: Any) -> None:
        async with init_redis_pool() as client:
            await client.set(key, value)

    async def get(self, key: Any) -> Any:
        async with init_redis_pool() as client:
            return await client.get(key)

    async def find(self, key: Any) -> Any:
        return await self.get(key)

    async def delete(self, *keys: list[Any]) -> None:
        async with init_redis_pool() as client:
            await client.delete(*keys)

    async def set_expiration(self, key: str, exp: int) -> None:
        async with init_redis_pool() as client:
            await client.expire(key, exp)
