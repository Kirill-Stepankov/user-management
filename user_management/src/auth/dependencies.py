from ..users.repository import UserRepository
from .service import AuthService


def auth_service():
    return AuthService(UserRepository)
