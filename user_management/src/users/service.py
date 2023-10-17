import uuid

from passlib.context import CryptContext
from src.repository import AbstractRepository

from .exceptions import UserAlreadyExistsException
from .schemas import UserAddSchema, UserOutputSchema, UserSchema, UserUpdateSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class HashPassword:
    @staticmethod
    def create_hash(password: str):
        return pwd_context.hash(password)

    @staticmethod
    def verify_hash(plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)


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

    async def get_user(self, uuid: uuid) -> UserSchema:
        user = await self.user_repo.get(uuid=uuid)
        return UserSchema.model_validate(user)

    async def patch_user(self, uuid: uuid, to_update: UserUpdateSchema) -> UserSchema:
        filtered = {
            key: value
            for key, value in to_update.model_dump().items()
            if value is not None
        }
        await self.user_repo.update(uuid, **filtered)
        return await self.get_user(uuid)
