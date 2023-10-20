from typing import Annotated, Any

from fastapi import APIRouter, Depends, File, Query, UploadFile
from fastapi.responses import JSONResponse
from pydantic import UUID4

from ..auth.dependencies import authenticate
from .dependencies import UserUpdateByAdminModel, UserUpdateModel, user_service
from .models import User
from .permissions import is_admin, is_moderator, is_users_moderator
from .schemas import UserSchema, UserUpdateByAdminSchema, UserUpdateSchema
from .service import UserService
from .utils import has_any_permissions

router = APIRouter(prefix="/user", tags=["users"])


@router.get("/me", response_model=UserSchema)
async def about_me(user: Annotated[User, Depends(authenticate)]) -> Any:
    return UserSchema.model_validate(user)


@router.patch("/me", response_model=UserSchema)
async def edit_about(
    user: Annotated[User, Depends(authenticate)],
    user_service: Annotated[UserService, Depends(user_service)],
    to_update: Annotated[UserUpdateSchema, Depends(UserUpdateModel)] = None,
    file: Annotated[bytes, File()] = None,
) -> Any:
    return await user_service.patch_user(user.uuid, to_update, file)


@router.delete("/me")
async def delete_me(
    user: Annotated[User, Depends(authenticate)],
    user_service: Annotated[UserService, Depends(user_service)],
):
    await user_service.delete_user(user.uuid)
    return JSONResponse(content={"detail": "User is successfully deleted."})


@router.get("/{user_id}", response_model=UserSchema)
@has_any_permissions([is_admin, is_users_moderator])
async def about_user(
    user_id: UUID4,
    user: Annotated[User, Depends(authenticate)],
    user_service: Annotated[UserService, Depends(user_service)],
):
    return await user_service.get_user(user_id)


@router.patch("/{user_id}")
@has_any_permissions([is_admin])
async def edit_user(
    user_id: UUID4,
    user: Annotated[User, Depends(authenticate)],
    user_service: Annotated[UserService, Depends(user_service)],
    to_update: Annotated[
        UserUpdateByAdminSchema, Depends(UserUpdateByAdminModel)
    ] = None,
    file: Annotated[bytes, File()] = None,
):
    return await user_service.patch_user(user_id, file)


@router.get("/")
@has_any_permissions([is_admin, is_moderator])
async def get_users(
    user: Annotated[User, Depends(authenticate)],
    user_service: Annotated[UserService, Depends(user_service)],
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1)] = 30,
    filter_by_name: Annotated[str, Query()] = None,
    sort_by: Annotated[str, Query()] = "username",
    order_by: Annotated[str, Query()] = "asc",
):
    users = await user_service.get_users(
        user, page, limit, filter_by_name, sort_by, order_by
    )
    return JSONResponse(content={"items": users, "page": page, "limit": limit})
