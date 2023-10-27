from abc import ABC
from datetime import datetime, timedelta

import jwt
from src.config import get_settings
from src.repository import AbstractRepository
from src.users.exceptions import (
    UserDoesNotExistException,
    UserInvalidCredentialsException,
)
from src.users.schemas import ResetPasswordSchema, UserAddSchema
from src.users.service import HashPassword

from .exceptions import NotRefreshTokenException, TokenIsBlacklistedException
from .utils import decode_token, send_reset_pass_email

settings = get_settings()


class AbstractAuthService(ABC):
    pass


class AuthService(AbstractAuthService):
    def __init__(self, user_repo: AbstractRepository, redis_repo: AbstractRepository):
        self.user_repo: AbstractRepository = user_repo
        self.redis_repo: AbstractRepository = redis_repo()

    def encode_token(self, payload: dict, expire):
        to_encode = payload.copy()
        to_encode.update({"exp": expire})

        encoded_token = jwt.encode(
            to_encode, settings.secret_key, algorithm=settings.crypt_algorithm
        )

        return encoded_token

    def token(self, payload: dict, is_access: bool = True):
        to_encode = payload.copy()
        to_encode.update({"is_access": is_access})

        expire = datetime.utcnow() + timedelta(
            minutes=(
                settings.access_token_timeout
                if is_access
                else settings.refresh_token_timeout
            )
        )

        encoded_jwt = self.encode_token(to_encode, expire)

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

    async def send_reset_request(self, email):
        user = await self.user_repo.get(email=email.email)
        if not user:
            raise UserDoesNotExistException("None")
        expire = datetime.utcnow() + timedelta(minutes=15)

        token = self.encode_token(payload={"uuid": user.uuid}, expire=expire)

        await send_reset_pass_email(email.email, token)

    async def reset_password(self, passwords: ResetPasswordSchema, token: str):
        payload = decode_token(token)

        uuid = payload.get("uuid")
        user = await self.user_repo.get(uuid=uuid)
        if user is None:
            raise UserDoesNotExistException("None")

        new_password = HashPassword.create_hash(passwords.password)
        await self.user_repo.update(uuid, hashed_password=new_password)
