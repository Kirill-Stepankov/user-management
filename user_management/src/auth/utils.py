import jwt
from fastapi import HTTPException, status

from ..config import get_settings

settings = get_settings()


def decode_token(token: str) -> dict:
    if token is None:
        raise HTTPException(status_code=401, detail="bb")
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
