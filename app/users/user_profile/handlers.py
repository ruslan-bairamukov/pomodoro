from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies import get_user_service
from app.users.auth.schemas import UserLoginSchema
from app.users.user_profile.schemas import UserCreateSchema
from app.users.user_profile.service import UserService

router = APIRouter(prefix="/user", tags=["user"])


@router.post(
    "",
    response_model=UserLoginSchema,
)
async def create_user(
    form_data: Annotated[
        OAuth2PasswordRequestForm, Depends()
    ],
    user_service: Annotated[
        UserService, Depends(get_user_service)
    ],
) -> UserLoginSchema:
    # TODO: add try-except to handle SQLAlchemy exception: not unique username
    user_in: UserCreateSchema = UserCreateSchema(
        username=form_data.username,
        password=form_data.password,
    )
    return await user_service.create_user(
        user_in=user_in,
    )
