from typing import Annotated

from fastapi import Depends

from cache_access import cache_helper
from data_access import db_helper
from repository import TaskCache, TaskRepository
from service import TaskService


def get_tasks_repository() -> TaskRepository:
    db_session = db_helper.session_factory()
    return TaskRepository(db_session)


def get_tasks_cache() -> TaskCache:
    redis_session = cache_helper.get_redis()
    return TaskCache(redis_session)


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
