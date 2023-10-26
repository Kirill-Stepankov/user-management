from fastapi import Header
from src.auth.service import AbstractAuthService
from src.users.service import AbstractUserService

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


def auth_service(async_session_maker):
    return AuthService(UserRepository(async_session_maker), RedisRepository)


async def authenticate(
    auth_serv: AbstractAuthService,
    user_serv: AbstractUserService,
    token: str = Header(),
) -> User:
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
