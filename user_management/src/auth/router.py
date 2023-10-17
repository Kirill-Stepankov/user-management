from typing import Annotated, Any

from fastapi import APIRouter, Depends, Header, status

from ..repository import RedisRepository
from ..users.dependencies import user_service
from ..users.schemas import UserAddSchema, UserOutputSchema
from ..users.service import UserService
from .dependencies import auth_service
from .service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/signup", response_model=UserOutputSchema, status_code=status.HTTP_201_CREATED
)
async def signup(
    user: UserAddSchema,
    user_service: Annotated[UserService, Depends(user_service)],
) -> Any:
    return await user_service.add_user(user)


@router.post("/login")
async def login(
    user: UserAddSchema, auth_service: Annotated[AuthService, Depends(auth_service)]
) -> dict:
    return await auth_service.login(user)


@router.post("/refresh-token")
async def refresh_token(
    auth_service: Annotated[AuthService, Depends(auth_service)],
    token: str = Header(),
) -> dict:
    return await auth_service.refresh_tokens(token)


@router.post("/reset-password")
async def reset_password():
    pass
