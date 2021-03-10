from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "The TipsChef API is running"}
