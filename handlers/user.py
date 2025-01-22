from typing import Annotated

from fastapi import APIRouter, Depends

from dependencies import get_user_service
from schemas import UserInSchema, UserOutSchema
from service import UserService

router = APIRouter(prefix="/user", tags=["user"])


@router.post(
    "",
    response_model=UserOutSchema,
)
async def create_user(
    user_in: UserInSchema,
    user_service: Annotated[
        UserService, Depends(get_user_service)
    ],
) -> UserOutSchema:
    return user_service.create_user(
        user_in=user_in,
    )
