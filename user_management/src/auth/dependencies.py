import jwt
from fastapi import Header, HTTPException, status

from ..config import get_settings
from ..users.exceptions import UserInvalidCredentialsException
from ..users.models import User
from ..users.repository import UserRepository
from .service import AuthService

settings = get_settings()


def auth_service():
    return AuthService(UserRepository)


async def authenticate(token: str = Header()) -> User:
    user_repo = UserRepository()
    if token is None:
        raise HTTPException(status_code=401, detail="bb")
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.crypt_algorithm]
        )
        uuid = payload.get("uuid")
    except jwt.exceptions.DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token."
        )
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired."
        )
    except jwt.exceptions.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="JWT error."
        )

    user = await user_repo.get(uuid=uuid)

    if user is None:
        raise UserInvalidCredentialsException

    return user
