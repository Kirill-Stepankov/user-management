from typing import Annotated, Any

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import UUID4

from ..auth.dependencies import authenticate
from .dependencies import user_service
from .models import User
from .permissions import is_admin, is_moderator
from .schemas import UserOutputSchema, UserSchema
from .service import UserService
from .utils import has_any_permissions

router = APIRouter(prefix="/user", tags=["users"])


@router.get("/me", response_model=UserSchema)
async def about_me(user: Annotated[User, Depends(authenticate)]) -> Any:
    return UserSchema.model_validate(user)


@router.patch("/me")
async def edit_about():
    pass


@router.delete("/me")
async def delete_me(
    user: Annotated[User, Depends(authenticate)],
    user_service: Annotated[UserService, Depends(user_service)],
):
    await user_service.delete_user(user.uuid)
    return JSONResponse(content={"detail": "User is successfully deleted."})


@router.get("/{user_id}", response_model=UserSchema)
@has_any_permissions([is_admin, is_moderator])
async def about_user(
    user_id: UUID4,
    user: Annotated[User, Depends(authenticate)],
    user_service: Annotated[UserService, Depends(user_service)],
):
    return await user_service.get_user(user_id)


@router.patch("/{user_id}")
async def edit_user():
    pass


@router.get("/")
async def get_users():
    pass
