from datetime import datetime, timedelta

from jose import jwt

from ..config import get_settings
from ..repository import AbstractRepository
from ..users.exceptions import (
    UserDoesNotExistException,
    UserInvalidCredentialsException,
)
from ..users.schemas import UserAddSchema
from ..users.utils import HashPassword

settings = get_settings()


class AuthService:
    def __init__(self, user_repo: AbstractRepository):
        self.user_repo: AbstractRepository = user_repo()

    def token(self, payload: dict, is_access: bool = True):
        to_encode = payload.copy()

        if is_access:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.access_token_timeout
            )
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.refresh_token_timeout
            )

        to_encode.update(
            {
                "exp": expire,
                "is_access": is_access,
            }
        )
        encoded_jwt = jwt.encode(
            to_encode, settings.secret_key, algorithm=settings.crypt_algorithm
        )

        return encoded_jwt

    def create_tokens(self, payload: dict):
        return {
            "access_token": self.token(payload),
            "refresh_token": self.token(payload, is_access=False),
        }

    async def login(self, user_add: UserAddSchema) -> dict:
        user = await self.user_repo.find(username=user_add.username)
        if not user:
            raise UserDoesNotExistException(user_add.username)

        user = user[0][0]
        if not HashPassword.verify_hash(user_add.hashed_password, user.hashed_password):
            raise UserInvalidCredentialsException(user.username)

        payload = {"user_id": user.uuid, "username": user.username}

        return self.create_tokens(payload)
