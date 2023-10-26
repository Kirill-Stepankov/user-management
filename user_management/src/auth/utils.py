import jwt
from fastapi import HTTPException, status
from src.database import aws_client

from ..config import get_settings

settings = get_settings()


def decode_token(token: str) -> dict:
    if token is None:
        raise HTTPException(status_code=401, detail="There is no token")
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.crypt_algorithm]
        )
    except jwt.exceptions.DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token."
        )
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired."
        )
    except jwt.exceptions.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="JWT error."
        )

    return payload


async def send_reset_pass_email(recipient, token):
    async with aws_client("ses") as ses:
        link = settings.reset_pass_url + "?" + token
        await ses.send_email(
            Source="kirillstepankov17@gmail.com",
            Destination={"ToAddresses": [recipient]},
            Message={
                "Subject": {"Data": "Reset password"},
                "Body": {"Text": {"Data": link}},
            },
        )
