from typing import Annotated

from email_validator import EmailNotValidError, validate_email
from fastapi import Depends, Form

from .enums import Role
from .exceptions import InvalidEmailException
from .repository import UserRepository
from .schemas import UserUpdateByAdminSchema, UserUpdateSchema
from .service import UserService


def user_service():
    return UserService(UserRepository)


def UserUpdateModel(
    username: Annotated[str, Form(min_length=1, max_length=255)] = None,
    name: Annotated[str, Form(min_length=1, max_length=255)] = None,
    email: Annotated[str, Form()] = None,
    surname: Annotated[str, Form(min_length=1, max_length=255)] = None,
    phone_number: Annotated[str, Form(min_length=4, max_length=30)] = None,
):
    try:
        if email:
            validate_email(email)
    except EmailNotValidError:
        raise InvalidEmailException

    return UserUpdateSchema(
        username=username,
        name=name,
        email=email,
        surname=surname,
        phone_number=phone_number,
    )


def UserUpdateByAdminModel(
    user_update: Annotated[UserUpdateSchema, Depends(UserUpdateModel)] = None,
    role: Annotated[Role | None, Form()] = None,
    is_blocked: Annotated[bool | None, Form()] = None,
):
    return UserUpdateByAdminSchema(
        **user_update.model_dump(), role=role, is_blocked=is_blocked
    )
