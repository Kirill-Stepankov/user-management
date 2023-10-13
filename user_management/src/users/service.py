from src.repository import AbstractRepository

from .exceptions import UserAlreadyExistsException
from .schemas import UserAddSchema, UserOutputSchema
from .utils import HashPassword


class UserService:
    def __init__(self, user_repo: AbstractRepository):
        self.user_repo: AbstractRepository = user_repo()

    async def add_user(self, user: UserAddSchema) -> UserOutputSchema:
        user_by_username = await self.user_repo.find(username=user.username)
        user_by_email = await self.user_repo.find(email=user.email)
        if user_by_email or user_by_username:
            raise UserAlreadyExistsException(user.username, user.email)

        user.hashed_password = HashPassword.create_hash(user.hashed_password)
        user_id = await self.user_repo.add_one(user.model_dump())

        return UserOutputSchema(uuid=user_id, **user.model_dump())
