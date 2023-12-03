from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from logs.logger import get_logger
from src.di import init_dependencies
from src.exception_handlers import init_exception_handlers
from src.users.models import User

from . import config
from .auth.router import router as auth_router
from .users.router import router as users_router

logger = get_logger()


def create_app():
    app = FastAPI()

    origins = [
        "http://localhost:5000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth_router)
    app.include_router(users_router)

    @app.get("/healthcheck")
    async def info(settings: Annotated[config.Settings, Depends(config.get_settings)]):
        logger.warning("TEST")

        return {
            "app_name": settings.logger_config_path,
        }

    init_dependencies(app)
    init_exception_handlers(app)

    return app
