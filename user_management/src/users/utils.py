from functools import wraps
from json import JSONEncoder
from uuid import UUID

from passlib.context import CryptContext

from .exceptions import UserDoesNotHavePermission
from .repository import UserRepository

old_default = JSONEncoder.default


def new_default(self, obj):
    if isinstance(obj, UUID):
        return str(obj)
    return old_default(self, obj)


JSONEncoder.default = new_default

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
            uuid = kwargs.get("user_id")
            user = kwargs.get("user")
            if uuid is not None:
                user_repo = UserRepository()
                user_by_uuid = await user_repo.get(uuid=uuid)
            for permission in permissions:
                if permission(user, object=user_by_uuid):
                    return await func(*args, **kwargs)
            raise UserDoesNotHavePermission

        return wrapper

    return inner
