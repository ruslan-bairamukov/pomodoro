from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from dependencies import get_auth_service
from exceptions import (
    UserIncorrectPasswordException,
    UserNotFoundException,
)
from schemas import UserInSchema, UserOutSchema
from service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "login",
    response_model=UserOutSchema,
)
async def login_user(
    user_in: UserInSchema,
    auth_service: Annotated[
        AuthService, Depends(get_auth_service)
    ],
) -> UserOutSchema:
    try:
        return auth_service.login(
            user_in=user_in,
        )
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except UserIncorrectPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
        )
