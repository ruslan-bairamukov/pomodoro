from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm

from dependencies import get_auth_service
from exceptions import (
    IncorrectPasswordError,
    UserNotFoundError,
)
from schemas import UserLoginSchema
from service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/token",
    response_model=UserLoginSchema,
)
async def login_for_access_token(
    form_data: Annotated[
        OAuth2PasswordRequestForm, Depends()
    ],
    auth_service: Annotated[
        AuthService, Depends(get_auth_service)
    ],
) -> UserLoginSchema:
    try:
        return auth_service.login_for_access_token(
            username=form_data.username,
            password=form_data.password,
        )
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except IncorrectPasswordError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
        )
