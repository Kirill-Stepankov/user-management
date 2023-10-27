from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from src.auth.exceptions import NotRefreshTokenException, TokenIsBlacklistedException
from src.users.exceptions import (
    InvalidEmailException,
    UserAlreadyExistsException,
    UserDoesNotExistException,
    UserDoesNotHavePermission,
    UserInvalidCredentialsException,
)


async def user_already_exists(request: Request, exc: UserAlreadyExistsException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": f"User with '{exc.username}' username is already registered."
        },
    )


async def user_does_not_exist(request: Request, exc: UserDoesNotExistException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": f"User with '{exc.username}' username isn't exist. Please register"
        },
    )


async def user_invalid_credentials(
    request: Request, exc: UserInvalidCredentialsException
):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": f"Invalid username or password."},
    )


async def user_does_not_have_permission(
    request: Request, exc: UserDoesNotHavePermission
):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": f"User doesn't have permission to access this resource."},
    )


async def not_refresh_token(request: Request, exc: NotRefreshTokenException):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": f"Given not resresh token for refresh."},
    )


async def token_is_blacklisted(request: Request, exc: TokenIsBlacklistedException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": f"Token is blacklisted."},
    )


async def invalid_email(request: Request, exc: InvalidEmailException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": f"Invalid email format."},
    )


def init_exception_handlers(app: FastAPI):
    app.exception_handler(UserAlreadyExistsException)(user_already_exists)
    app.exception_handler(UserDoesNotExistException)(user_does_not_exist)
    app.exception_handler(UserInvalidCredentialsException)(user_invalid_credentials)
    app.exception_handler(UserDoesNotHavePermission)(user_does_not_have_permission)
    app.exception_handler(NotRefreshTokenException)(not_refresh_token)
    app.exception_handler(TokenIsBlacklistedException)(token_is_blacklisted)
    app.exception_handler(InvalidEmailException)(invalid_email)
