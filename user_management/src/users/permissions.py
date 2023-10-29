from .enums import Role
from .models import User


class BasePermission:
    def has_permission(user: User, **kwargs) -> bool:
        pass


class IsAdmin(BasePermission):
    def has_permission(user: User, **kwargs) -> bool:
        return user.role == Role.ADMIN


class IsModerator(BasePermission):
    def has_permission(user: User, **kwargs) -> bool:
        return user.role == Role.MODERATOR


class IsUsersModerator(BasePermission):
    def has_permission(user: User, **kwargs) -> bool:
        object = kwargs.get("object")
        if user.role == Role.MODERATOR:
            return user.group_id == object.group_id
        return False


class IsUser(BasePermission):
    def has_permission(user: User, **kwargs) -> bool:
        return user.role == Role.USER
