from typing import Annotated, Any

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import (
    HTTPBearer,
    OAuth2PasswordBearer,
)
from redis import Redis
from sqlalchemy.orm import Session

from cache_access import cache_helper
from clients import GoogleClient, YandexClient
from config import settings
from data_access import db_helper
from exceptions import InvalidJWTTokenError
from repository import (
    TaskCache,
    TaskRepository,
    UserRepository,
)
from service import AuthService, TaskService, UserService

oauth2_scheme = HTTPBearer()


def get_tasks_repository(
    db_session: Annotated[
        Session, Depends(db_helper.get_db_session)
    ],
) -> TaskRepository:
    return TaskRepository(
        db_session=db_session,
    )


def get_tasks_cache(
    redis: Annotated[
        Redis, Depends(cache_helper.get_redis)
    ],
) -> TaskCache:
    return TaskCache(
        redis=redis,
    )


def get_tasks_service(
    task_repository: Annotated[
        TaskRepository, Depends(get_tasks_repository)
    ],
    task_cache: Annotated[
        TaskCache, Depends(get_tasks_cache)
    ],
) -> TaskService:
    return TaskService(
        task_repository=task_repository,
        task_cache=task_cache,
    )


def get_user_repository(
    db_session: Annotated[
        Session, Depends(db_helper.get_db_session)
    ],
) -> UserRepository:
    return UserRepository(
        db_session=db_session,
    )


def get_google_client() -> GoogleClient:
    return GoogleClient(settings=settings)


def get_yandex_client() -> YandexClient:
    return YandexClient(settings=settings)


def get_auth_service(
    user_repository: Annotated[
        UserRepository,
        Depends(get_user_repository),
    ],
) -> AuthService:
    return AuthService(user_repository=user_repository)


def get_user_service(
    user_repository: Annotated[
        UserRepository,
        Depends(get_user_repository),
    ],
    auth_service: Annotated[
        AuthService, Depends(get_auth_service)
    ],
):
    return UserService(
        user_repository=user_repository,
        auth_service=auth_service,
    )


def get_jwt_payload(
    token: Annotated[
        OAuth2PasswordBearer, Depends(oauth2_scheme)
    ],
    auth_service: Annotated[
        AuthService, Depends(get_auth_service)
    ],
) -> dict[str, Any]:
    try:
        return auth_service.validate_jwt(
            token=token.credentials
        )
    except jwt.PyJWTError:
        raise InvalidJWTTokenError


def get_current_user_id(
    payload: Annotated[
        dict[str, Any], Depends(get_jwt_payload)
    ],
) -> int:
    try:
        user_id = int(payload.get("sub"))
    except InvalidJWTTokenError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error.message,
        )
    return user_id
