from typing import Annotated

from fastapi import APIRouter, Depends, status

from data_access.db_helper import db_helper
from dependencies.dependencies import (
    get_tasks_repository,
    get_tasks_service,
)

# from dependencies.fake_data import fake_tasks
# from dependencies.util import find_task_by_id
from repository import TaskRepository
from schemas.task import TaskSchema
from service import TaskService

router = APIRouter(
    prefix="/tasks",
    tags=["task"],
)


get_db_connection = db_helper.session_factory


@router.get(
    "/all",
    response_model=list[TaskSchema],
    status_code=status.HTTP_200_OK,
)
async def get_tasks(
    task_service: Annotated[
        TaskService, Depends(get_tasks_service)
    ],
) -> list[TaskSchema]:
    return task_service.get_tasks()


@router.get(
    "/{task_id}",
    response_model=TaskSchema,
    status_code=status.HTTP_200_OK,
)
async def get_task_by_id(
    task_id: int,
    task_repository: Annotated[
        TaskRepository, Depends(get_tasks_repository)
    ],
):
    task = task_repository.get_task_by_id(task_id)
    return task


@router.post(
    "/",
    response_model=TaskSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    task_in: TaskSchema,
    task_repository: Annotated[
        TaskRepository, Depends(get_tasks_repository)
    ],
):
    task_model = task_repository.create_task(task_in)
    task = TaskSchema.model_validate(task_model)
    return task


@router.patch(
    "/{task_id}",
    response_model=TaskSchema,
    status_code=status.HTTP_200_OK,
)
async def update_task(
    task_id: int,
    task_update: TaskSchema,
    task_repository: Annotated[
        TaskRepository, Depends(get_tasks_repository)
    ],
):
    task_model = task_repository.update_task(
        task_id, task_update
    )
    task = TaskSchema.model_validate(task_model)
    return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(
    task_id: int,
    task_repository: Annotated[
        TaskRepository, Depends(get_tasks_repository)
    ],
):
    task_repository.delete_task(task_id)
    return {
        "message": f"task {task_id} deleted successfully"
    }
