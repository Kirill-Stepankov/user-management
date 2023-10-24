from typing import Annotated, Any

from fastapi import APIRouter, Depends, Header, Query, status
from fastapi.responses import JSONResponse

from ..users.schemas import (
    EmailSchema,
    ResetPasswordSchema,
    UserAddSchema,
    UserOutputSchema,
)
from ..users.service import AbstractUserService
from .service import AbstractAuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/signup", response_model=UserOutputSchema, status_code=status.HTTP_201_CREATED
)
async def signup(
    user: UserAddSchema,
    user_service: AbstractUserService = Depends(),
) -> Any:
    return await user_service.add_user(user)


@router.post("/login")
async def login(
    user: UserAddSchema, auth_service: AbstractAuthService = Depends()
) -> dict:
    return await auth_service.login(user)


@router.post("/refresh-token")
async def refresh_token(
    auth_service: AbstractAuthService = Depends(),
    token: str = Header(),
) -> dict:
    return await auth_service.refresh_tokens(token)


@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(
    email: EmailSchema, auth_service: AbstractAuthService = Depends()
):
    await auth_service.send_reset_request(email)
    return JSONResponse(
        content={"detail": "Email is sent."}, status_code=status.HTTP_200_OK
    )


@router.post("/change-password")
async def change_password(
    token: Annotated[str, Query()],
    passwords: ResetPasswordSchema,
    auth_service: AbstractAuthService = Depends(),
):
    await auth_service.reset_password(passwords, token)

    return JSONResponse(
        content={"detail": "Password is changed."}, status_code=status.HTTP_201_CREATED
    )
