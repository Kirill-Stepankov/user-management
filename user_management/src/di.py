from functools import partial
from typing import Any

from fastapi import FastAPI, Header
from src.abstract import authenticate_stub
from src.auth.dependencies import auth_service, authenticate
from src.auth.service import AbstractAuthService
from src.users.dependencies import user_service
from src.users.service import AbstractUserService

from .database import create_session_maker


class AuthenticatePartial:
    def __init__(
        self,
        auth_serv: AbstractAuthService,
        user_serv: AbstractUserService,
    ) -> None:
        self.auth_serv = auth_serv
        self.user_serv = user_serv

    async def __call__(self, token: str = Header()):
        return await authenticate(self.user_serv, self.auth_serv, token)


def init_dependencies(app: FastAPI):
    session_maker = create_session_maker()

    app.dependency_overrides[AbstractUserService] = partial(user_service, session_maker)
    app.dependency_overrides[AbstractAuthService] = partial(auth_service, session_maker)
    app.dependency_overrides[authenticate_stub] = AuthenticatePartial(
        user_service(session_maker), auth_service(session_maker)
    )
