from typing import Annotated, Any

from fastapi import APIRouter, Depends

from ..users.dependencies import user_service
from ..users.schemas import UserAddSchema, UserOutputSchema
from ..users.service import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=UserOutputSchema)
async def about_me(
    user: UserAddSchema,
    user_service: Annotated[UserService, Depends(user_service)],
) -> Any:
    return await user_service.add_user(user)


@router.post("/login")
async def login():
    pass


@router.post("/refresh-token")
async def refresh_token():
    pass


@router.post("/reset-password")
async def reset_password():
    pass
