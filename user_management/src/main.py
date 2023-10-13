from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from logs.logger import get_logger
from typing_extensions import Annotated

from . import config
from .auth.router import router as auth_router
from .users.exceptions import UserAlreadyExistsException
from .users.router import router as users_router

logger = get_logger()
app = FastAPI()

app.include_router(auth_router)
app.include_router(users_router)


@app.get("/healthcare")
async def info(settings: Annotated[config.Settings, Depends(config.get_settings)]):
    logger.warning("TEST")
    return {
        "app_name": settings.logger_config_path,
    }


@app.exception_handler(UserAlreadyExistsException)
async def unicorn_exception_handler(request: Request, exc: UserAlreadyExistsException):
    return JSONResponse(
        status_code=400,
        content={
            "detail": f"User with '{exc.username}' username is already registered."
        },
    )
