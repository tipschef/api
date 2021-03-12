from fastapi import APIRouter

router = APIRouter(prefix='/users')


@router.get("/")
async def user_route():
    return {"message": "User route"}
