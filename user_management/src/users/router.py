from fastapi import APIRouter

router = APIRouter(prefix="/user", tags=["users"])


@router.get("/me")
async def about_me():
    pass


@router.patch("/me")
async def edit_about():
    pass


@router.delete("/me")
async def delete_me():
    pass


@router.get("/{user_id}")
async def about_user():
    pass


@router.patch("/{user_id}")
async def edit_user():
    pass


@router.get("/")
async def get_users():
    pass
