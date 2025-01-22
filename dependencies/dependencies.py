from typing import Annotated

from fastapi import Depends
from redis import Redis
from sqlalchemy.orm import Session

from cache_access import cache_helper
from data_access import db_helper
from repository import TaskCache, TaskRepository
from service import (
    AuthService,
    TaskService,
    UserRepository,
    UserService,
)


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


def get_user_service(
    user_repository: Annotated[
        UserRepository,
        Depends(get_user_repository),
    ],
):
    return UserService(
        user_repository=user_repository,
    )


def get_auth_service(
    user_repository: Annotated[
        UserRepository,
        Depends(get_user_repository),
    ],
) -> AuthService:
    return AuthService(
        user_repository=user_repository,
    )
