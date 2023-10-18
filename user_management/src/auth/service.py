from datetime import datetime, timedelta

import jwt

from ..config import get_settings
from ..repository import AbstractRepository
from ..users.exceptions import (
    UserDoesNotExistException,
    UserInvalidCredentialsException,
)
from ..users.schemas import UserAddSchema
from ..users.service import HashPassword
from .exceptions import NotRefreshTokenException, TokenIsBlacklistedException
from .utils import decode_token

settings = get_settings()


class AuthService:
    def __init__(self, user_repo: AbstractRepository, redis_repo: AbstractRepository):
        self.user_repo: AbstractRepository = user_repo()
        self.redis_repo: AbstractRepository = redis_repo()

    def token(self, payload: dict, is_access: bool = True):
        to_encode = payload.copy()

        expire = datetime.utcnow() + timedelta(
            minutes=(
                settings.access_token_timeout
                if is_access
                else settings.refresh_token_timeout
            )
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
        user = await self.user_repo.get(username=user_add.username)
        if not user:
            raise UserDoesNotExistException(user_add.username)

        if not HashPassword.verify_hash(user_add.hashed_password, user.hashed_password):
            raise UserInvalidCredentialsException(user.username)

        payload = {"uuid": user.uuid, "username": user.username}

        return self.create_tokens(payload)

    async def refresh_tokens(self, token: str) -> dict:
        is_blacklisted = await self.token_is_blacklisted(token)
        if is_blacklisted:
            raise TokenIsBlacklistedException
        payload = decode_token(token)
        uuid = payload.get("uuid")
        is_access = payload.get("is_access")

        if is_access:
            raise NotRefreshTokenException

        await self.redis_repo.add_one_with_expiration(
            token, uuid, settings.refresh_token_timeout * 60
        )

        return self.create_tokens(payload)

    async def token_is_blacklisted(self, token: str) -> bool:
        return bool(await self.redis_repo.get(token))
