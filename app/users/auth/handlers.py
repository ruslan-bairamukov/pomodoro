from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies import (
    get_auth_service,
    get_google_client,
    get_yandex_client,
)
from app.exceptions import (
    IncorrectPasswordError,
    UserNotFoundError,
)
from app.users.auth.clients.google import GoogleClient
from app.users.auth.clients.yandex import YandexClient
from app.users.auth.schemas import UserLoginSchema
from app.users.auth.service import AuthService

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
        return await auth_service.password_login(
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
async def google_login(
    auth_service: Annotated[
        AuthService, Depends(get_auth_service)
    ],
) -> RedirectResponse:
    redirect_url = (
        await auth_service.get_google_redirect_url()
    )
    print(f"\n\n{redirect_url = }\n\n")
    return RedirectResponse(url=redirect_url)


@router.get(
    "/google",
)
async def google_auth(
    auth_service: Annotated[
        AuthService, Depends(get_auth_service)
    ],
    code: str,
    google_client: Annotated[
        GoogleClient, Depends(get_google_client)
    ],
):
    return await auth_service.oidc_login(
        code=code,
        oidc_client=google_client,
    )


@router.get(
    "/login/yandex",
    response_class=RedirectResponse,
)
async def yandex_login(
    auth_service: Annotated[
        AuthService, Depends(get_auth_service)
    ],
) -> RedirectResponse:
    redirect_url = (
        await auth_service.get_yandex_redirect_url()
    )
    print(f"\n\n{redirect_url = }\n\n")
    return RedirectResponse(url=redirect_url)


@router.get(
    "/yandex",
)
async def yandex_auth(
    auth_service: Annotated[
        AuthService, Depends(get_auth_service)
    ],
    code: str,
    yandex_client: Annotated[
        YandexClient, Depends(get_yandex_client)
    ],
):
    return await auth_service.oidc_login(
        code=code,
        oidc_client=yandex_client,
    )
