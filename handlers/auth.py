from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm

from clients import GoogleClient
from dependencies import (
    get_auth_service,
    get_google_client,
    get_yandex_client,
)
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
async def password_login(
    form_data: Annotated[
        OAuth2PasswordRequestForm, Depends()
    ],
    auth_service: Annotated[
        AuthService, Depends(get_auth_service)
    ],
) -> UserLoginSchema:
    try:
        return auth_service.password_login(
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


@router.get(
    "/login/google",
    response_class=RedirectResponse,
)
def google_login(
    auth_service: Annotated[
        AuthService, Depends(get_auth_service)
    ],
) -> RedirectResponse:
    redirect_url = auth_service.get_google_redirect_url()
    print(f"\n\n{redirect_url = }\n\n")
    return RedirectResponse(url=redirect_url)


@router.get(
    "/google",
)
def google_auth(
    auth_service: Annotated[
        AuthService, Depends(get_auth_service)
    ],
    code: str,
    google_client: Annotated[
        GoogleClient, Depends(get_google_client)
    ],
):
    return auth_service.oidc_login(
        code=code,
        oidc_client=google_client,
    )


@router.get(
    "/login/yandex",
    response_class=RedirectResponse,
)
def yandex_login(
    auth_service: Annotated[
        AuthService, Depends(get_auth_service)
    ],
) -> RedirectResponse:
    redirect_url = auth_service.get_yandex_redirect_url()
    print(f"\n\n{redirect_url = }\n\n")
    return RedirectResponse(url=redirect_url)


@router.get(
    "/yandex",
)
def yandex_auth(
    auth_service: Annotated[
        AuthService, Depends(get_auth_service)
    ],
    code: str,
    yandex_client: Annotated[
        GoogleClient, Depends(get_yandex_client)
    ],
):
    return auth_service.oidc_login(
        code=code,
        oidc_client=yandex_client,
    )
