import uuid

from src.repository import AbstractRepository

from .exceptions import UserAlreadyExistsException
from .schemas import UserAddSchema, UserOutputSchema
from .utils import HashPassword


class UserService:
    def __init__(self, user_repo: AbstractRepository):
        self.user_repo: AbstractRepository = user_repo()

    async def add_user(self, user: UserAddSchema) -> UserOutputSchema:
        user_by_username = await self.user_repo.get(username=user.username)
        if user_by_username:
            raise UserAlreadyExistsException(user.username)

        user.hashed_password = HashPassword.create_hash(user.hashed_password)
        user_id = await self.user_repo.add_one(user.model_dump())

        return UserOutputSchema(uuid=user_id, **user.model_dump())

    async def delete_user(self, uuid: uuid):
        await self.user_repo.delete(uuid=uuid)
