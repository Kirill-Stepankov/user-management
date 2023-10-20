from fastapi import Header, HTTPException, status

from ..config import get_settings
from ..repository import RedisRepository
from ..users.dependencies import user_service
from ..users.exceptions import UserInvalidCredentialsException
from ..users.models import User
from ..users.repository import UserRepository
from .exceptions import TokenIsBlacklistedException
from .service import AuthService
from .utils import decode_token

settings = get_settings()


def auth_service():
    return AuthService(UserRepository, RedisRepository)


async def authenticate(token: str = Header()) -> User:
    auth_serv = auth_service()
    user_serv = user_service()
    is_blacklisted = await auth_serv.token_is_blacklisted(token)
    if is_blacklisted:
        raise TokenIsBlacklistedException
    payload = decode_token(token)
    uuid = payload.get("uuid")

    is_access = payload.get("is_access")
    if is_access is None:
        raise UserInvalidCredentialsException

    user = await user_serv.get_user(uuid=uuid)
    if user is None:
        raise UserInvalidCredentialsException

    return user
