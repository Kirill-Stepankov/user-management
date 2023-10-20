import uuid

import botocore
from fastapi import UploadFile
from passlib.context import CryptContext
from src.repository import AbstractRepository, S3_repository

from .enums import Role
from .exceptions import UserAlreadyExistsException, UserDoesNotExistException
from .models import User
from .schemas import (
    UserAddSchema,
    UserOutputSchema,
    UserSchema,
    UserUpdateByAdminSchema,
    UserUpdateSchema,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class HashPassword:
    @staticmethod
    def create_hash(password: str):
        return pwd_context.hash(password)

    @staticmethod
    def verify_hash(plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)


class UserService:
    def __init__(self, user_repo: AbstractRepository, s3_repo: AbstractRepository):
        self.user_repo: AbstractRepository = user_repo()
        self.s3_repo: AbstractRepository = s3_repo()

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
        if user is None:
            raise UserDoesNotExistException("None")
        return UserSchema.model_validate(user)

    async def patch_user(
        self,
        uuid: uuid,
        to_update: UserUpdateSchema | UserUpdateByAdminSchema,
        file: bytes,
    ) -> UserSchema:
        filtered = {
            key: value
            for key, value in to_update.model_dump().items()
            if value is not None
        }
        if file:
            filtered["s3_path"] = str(uuid)

            is_exists = True
            try:
                await self.s3_repo.get(str(uuid))
            except botocore.exceptions.ClientError:
                is_exists = False

            if is_exists:
                await self.s3_repo.delete(str(uuid))

            await self.s3_repo.add_one(file, str(uuid))

        await self.user_repo.update(uuid, **filtered)
        return await self.get_user(uuid)

    async def get_users(
        self,
        owner: User,
        page: int,
        limit: int,
        filter_by_name: str,
        sort_by: str,
        order_by: str,
    ) -> list[dict]:
        is_admin = owner.role == Role.ADMIN
        group_id = owner.group_id

        users = await self.user_repo.find(
            page, limit, filter_by_name, sort_by, order_by, is_admin, group_id=group_id
        )
        return [UserSchema.model_validate(user).model_dump() for user in users]
