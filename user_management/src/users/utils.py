from datetime import datetime
from functools import wraps
from json import JSONEncoder
from uuid import UUID

from .dependencies import user_service
from .enums import Role
from .exceptions import UserDoesNotHavePermission
from .permissions import BasePermission

old_default = JSONEncoder.default


def new_default(self, obj):
    if isinstance(obj, UUID):
        return str(obj)
    if isinstance(obj, Role):
        return obj.value
    if isinstance(obj, datetime):
        return str(obj)
    return old_default(self, obj)


JSONEncoder.default = new_default


def has_any_permissions(permissions: list[BasePermission]):
    def inner(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            uuid = kwargs.get("user_id")
            user = kwargs.get("user")
            user_by_uuid = None
            if uuid is not None:
                user_serv = kwargs.get("user_service")
                user_by_uuid = await user_serv.get_user(uuid)
            for permission in permissions:
                if permission.has_permission(user, object=user_by_uuid):
                    return await func(*args, **kwargs)
            raise UserDoesNotHavePermission

        return wrapper

    return inner
