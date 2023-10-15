from typing import Annotated, Any

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from ..auth.dependencies import authenticate
from .dependencies import user_service
from .models import User
from .schemas import UserOutputSchema, UserSchema
from .service import UserService

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


@router.get("/{user_id}")
async def about_user():
    pass


@router.patch("/{user_id}")
async def edit_user():
    pass


@router.get("/")
async def get_users():
    pass
