from fastapi import Depends, FastAPI, Request, status
from fastapi.responses import JSONResponse
from logs.logger import get_logger
from typing_extensions import Annotated

from . import config
from .auth.exceptions import NotRefreshTokenException, TokenIsBlacklistedException
from .auth.router import router as auth_router
from .users.exceptions import (
    InvalidEmailException,
    UserAlreadyExistsException,
    UserDoesNotExistException,
    UserDoesNotHavePermission,
    UserInvalidCredentialsException,
)
from .users.router import router as users_router

logger = get_logger()
app = FastAPI()

app.include_router(auth_router)
app.include_router(users_router)


@app.exception_handler(UserAlreadyExistsException)
async def unicorn_exception_handler(request: Request, exc: UserAlreadyExistsException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": f"User with '{exc.username}' username is already registered."
        },
    )


@app.exception_handler(UserDoesNotExistException)
async def unicorn_exception_handler(request: Request, exc: UserDoesNotExistException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": f"User with '{exc.username}' username isn't exist. Please register"
        },
    )


@app.exception_handler(UserInvalidCredentialsException)
async def unicorn_exception_handler(
    request: Request, exc: UserInvalidCredentialsException
):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": f"Invalid username or password."},
    )


@app.exception_handler(UserDoesNotHavePermission)
async def unicorn_exception_handler(request: Request, exc: UserDoesNotHavePermission):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": f"User doesn't have permission to access this resource."},
    )


@app.exception_handler(NotRefreshTokenException)
async def unicorn_exception_handler(request: Request, exc: NotRefreshTokenException):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": f"Given not resresh token for refresh."},
    )


@app.exception_handler(TokenIsBlacklistedException)
async def unicorn_exception_handler(request: Request, exc: TokenIsBlacklistedException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": f"Token is blacklisted."},
    )


@app.exception_handler(InvalidEmailException)
async def unicorn_exception_handler(request: Request, exc: TokenIsBlacklistedException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": f"Invalid email format."},
    )


@app.get("/healthcheck")
async def info(settings: Annotated[config.Settings, Depends(config.get_settings)]):
    logger.warning("TEST")

    return {
        "app_name": settings.logger_config_path,
    }
