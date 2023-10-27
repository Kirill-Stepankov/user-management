from abc import ABC, abstractmethod

from fastapi import Header


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one():
        pass

    @abstractmethod
    async def find():
        pass

    @abstractmethod
    async def get():
        pass

    @abstractmethod
    async def delete():
        pass


async def authenticate_stub(token: str = Header()):
    raise NotImplementedError
