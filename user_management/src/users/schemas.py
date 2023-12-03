from datetime import datetime
from typing import Annotated

from email_validator import EmailNotValidError, validate_email
from pydantic import UUID4, BaseModel, ConfigDict, Field, field_validator

from .enums import Role


class UserBaseSchema(BaseModel):
    username: str = Field(max_length=255, min_length=1)


class UserAddSchema(UserBaseSchema):
    hashed_password: str = Field(max_length=155, min_length=8)


class UserOutputSchema(UserBaseSchema):
    uuid: UUID4


class UserUpdateSchema(UserBaseSchema):
    username: str | None = None
    name: str | None = None
    email: str | None = None
    surname: str | None = None
    phone_number: str | None = None


class UserUpdateByAdminSchema(UserUpdateSchema):
    role: Role | None = None
    is_blocked: bool | None = Field(default=False)


class EmailSchema(BaseModel):
    email: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        if value is None:
            return value
        try:
            validate_email(value)
        except EmailNotValidError:
            raise ValueError("Invalid email format")
        return value


class UserSchema(UserBaseSchema, EmailSchema):
    uuid: UUID4
    name: str | None = Field(max_length=255, min_length=1)
    email: str | None = None
    surname: str | None = Field(max_length=255, min_length=1)
    phone_number: str | None = Field(min_length=4, max_length=30)
    role: Role | None = None
    group_id: int | None = None
    is_blocked: bool = Field(default=False)
    created_at: datetime
    updated_at: datetime
    s3_path: str | None = None

    model_config = ConfigDict(from_attributes=True)


class UserWithAvatarSchema(UserSchema):
    image: bytes | None = None


class ResetPasswordSchema(BaseModel):
    password: str = Field(min_length=8)
    repeat_password: str = Field(min_length=8)

    @field_validator("repeat_password")
    @classmethod
    def validate_pass(cls, value, values):
        passw = values.data.get("password")
        if value != passw:
            raise ValueError("Passwords aren't equal.")
        return value
