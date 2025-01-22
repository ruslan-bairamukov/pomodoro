from dependencies.dependencies import (
    get_auth_service,
    get_tasks_cache,
    get_tasks_repository,
    get_tasks_service,
    get_user_repository,
    get_user_service,
)

__all__ = [
    "get_auth_service",
    "get_tasks_service",
    "get_tasks_repository",
    "get_tasks_cache",
    "get_user_repository",
    "get_user_service",
]
