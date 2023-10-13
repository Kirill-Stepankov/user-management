from datetime import datetime

from email_validator import EmailNotValidError, validate_email
from pydantic import UUID4, BaseModel, Field, field_validator

from .utils import Role


class UserBaseSchema(BaseModel):
    username: str = Field(max_length=255)
    email: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        try:
            validate_email(value)
        except EmailNotValidError:
            raise ValueError("Invalid email format")
        return value


class UserAddSchema(UserBaseSchema):
    hashed_password: str = Field(max_length=155, min_length=8)


class UserOutputSchema(UserBaseSchema):
    uuid: UUID4


class UserSchema(UserBaseSchema):
    uuid: UUID4
    name: str = Field(max_length=255)
    surname: str = Field(max_length=255)
    phone_number: str = Field(min_length=4, max_length=30)
    role: Role
    group_id: int
    is_blocked: bool = Field(default=False)
    created_at: datetime
    updated_at: datetime
    s3_path: str
