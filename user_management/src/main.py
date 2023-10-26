from fastapi import FastAPI
from src.di import init_dependencies
from src.exception_handlers import init_exception_handlers
from src.routers import init_routers
from src.users.models import User


def create_app():
    app = FastAPI()

    init_routers(app)
    init_dependencies(app)
    init_exception_handlers(app)

    return app
