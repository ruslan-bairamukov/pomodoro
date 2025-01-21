from fastapi import APIRouter

from config import settings

router = APIRouter(
    prefix="/ping",
    tags=["ping"],
)


@router.get("/db")
async def ping_db():
    return {"message": settings.GOOGLE_TOKEN_ID}


@router.get("/app")
async def ping_app():
    return {"message": "app is working"}
