import enum

from passlib.context import CryptContext


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
