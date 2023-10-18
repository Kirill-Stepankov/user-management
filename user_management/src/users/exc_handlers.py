from fastapi import Request
from fastapi.responses import JSONResponse

from .exceptions import UserAlreadyExistsException
from .router import router


@router.exception_handler(UserAlreadyExistsException)
async def unicorn_exception_handler(request: Request, exc: UserAlreadyExistsException):
    return JSONResponse(
        status_code=400,
        content={
            "detail": f"User with '{exc.username}' username or '{exc.email}' email is already registered"
        },
    )
