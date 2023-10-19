from .enums import Role
from .models import User


def is_admin(user: User, **kwargs) -> bool:
    return user.role == Role.ADMIN


def is_moderator(user: User, **kwargs) -> bool:
    return user.role == Role.MODERATOR


def is_users_moderator(user: User, **kwargs) -> bool:
    object = kwargs.get("object")
    if user.role == Role.MODERATOR:
        return user.group_id == object.group_id
    return False


def is_user(user: User, **kwargs) -> bool:
    return user.role == Role.USER
