from src.repository import SQLAlchemyRepository

from .models import User


class UserRepository(SQLAlchemyRepository):
    model = User
