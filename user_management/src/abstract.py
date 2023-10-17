from abc import ABC, abstractmethod


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
