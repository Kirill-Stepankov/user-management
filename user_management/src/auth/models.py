import enum
import uuid
from datetime import datetime

from sqlalchemy import UUID, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class Role(enum.Enum):
    USER = "User"
    ADMIN = "Admin"
    MODERATOR = "Moderator"


class Group(Base):
    __tablename__ = "group"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text, unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, index=True
    )


class User(Base):
    __tablename__ = "user"

    uuid: Mapped[uuid] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(Text)
    surname: Mapped[str] = mapped_column(Text)
    username: Mapped[str] = mapped_column(Text, unique=True, index=True)
    email: Mapped[str] = mapped_column(Text, unique=True, index=True)
    phone_number: Mapped[str] = mapped_column(Text)
    role: Mapped[Role]
    group_id: Mapped[int] = mapped_column(ForeignKey("group.id"))
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    s3_path: Mapped[str] = mapped_column(Text)
