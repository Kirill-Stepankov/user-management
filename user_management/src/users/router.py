from typing import Annotated, Any

from fastapi import APIRouter, Depends

from ..auth.dependencies import authenticate
from .models import User
from .schemas import UserOutputSchema, UserSchema

router = APIRouter(prefix="/user", tags=["users"])


@router.get("/me", response_model=UserSchema)
async def about_me(user: Annotated[User, Depends(authenticate)]) -> Any:
    return UserSchema.model_validate(user)


@router.patch("/me")
async def edit_about():
    pass


@router.delete("/me")
async def delete_me():
    pass


@router.get("/{user_id}")
async def about_user():
    pass


@router.patch("/{user_id}")
async def edit_user():
    pass


@router.get("/")
async def get_users():
    pass
