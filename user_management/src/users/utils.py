import enum
from functools import wraps
from json import JSONEncoder
from uuid import UUID

from passlib.context import CryptContext

from .exceptions import UserDoesNotHavePermission

old_default = JSONEncoder.default


def new_default(self, obj):
    if isinstance(obj, UUID):
        return str(obj)
    return old_default(self, obj)


JSONEncoder.default = new_default


class Role(enum.Enum):
    USER = "User"
    ADMIN = "Admin"
    MODERATOR = "Moderator"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class HashPassword:
    @staticmethod
    def create_hash(password: str):
        return pwd_context.hash(password)

    @staticmethod
    def verify_hash(plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)


def has_any_permissions(permissions: list[callable]):
    def inner(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for permission in permissions:
                if permission(kwargs["user"]):
                    return await func(*args, **kwargs)
            raise UserDoesNotHavePermission

        return wrapper

    return inner
