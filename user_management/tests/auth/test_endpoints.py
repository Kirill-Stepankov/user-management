from httpx import AsyncClient
from src.users.schemas import UserAddSchema


async def test_signup(
    ac: AsyncClient,
):
    user_add_credentials = UserAddSchema(
        username="kirill",
        hashed_password="password",
    )

    response = await ac.post(
        "/auth/signup", data=user_add_credentials.model_dump_json()
    )

    assert response.status_code == 201
    assert response.json().get("username") == "kirill"
