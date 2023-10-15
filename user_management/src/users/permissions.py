from .models import User
from .utils import Role


def is_admin(user: User) -> bool:
    return user.role == Role.ADMIN


def is_moderator(user: User) -> bool:
    return user.role == Role.MODERATOR


def is_user(user: User) -> bool:
    return user.role == Role.USER
