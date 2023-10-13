from .repository import UserRepository
from .service import UserService


def user_service():
    return UserService(UserRepository)
