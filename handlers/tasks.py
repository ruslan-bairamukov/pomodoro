from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from dependencies import (
    get_current_user_id,
    get_tasks_service,
)
from exceptions import TaskNotFoundError
from schemas import TaskCreateSchema, TaskSchema
from service import TaskService

router = APIRouter(
    prefix="/tasks",
    tags=["task"],
)


@router.get(
    "/all",
    response_model=list[TaskSchema],
    status_code=status.HTTP_200_OK,
)
async def get_tasks(
    task_service: Annotated[
        TaskService, Depends(get_tasks_service)
    ],
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> list[TaskSchema]:
    tasks = await task_service.get_tasks(user_id=user_id)
    return tasks


@router.get(
    "/{task_id}",
    response_model=TaskSchema,
    status_code=status.HTTP_200_OK,
)
async def get_task_by_id(
    task_id: int,
    task_service: Annotated[
        TaskService, Depends(get_tasks_service)
    ],
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> TaskSchema:
    try:
        task = await task_service.get_task_by_id(
            task_id=task_id,
            user_id=user_id,
        )
    except TaskNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error.message,
        )
    return task


@router.post(
    "/",
    response_model=TaskSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    task_in: TaskCreateSchema,
    task_service: Annotated[
        TaskService, Depends(get_tasks_service)
    ],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    task = await task_service.create_task(
        task_in=task_in, user_id=user_id
    )
    return task


@router.patch(
    "/{task_id}",
    response_model=TaskSchema,
    status_code=status.HTTP_200_OK,
)
async def update_task(
    task_id: int,
    task_update: TaskCreateSchema,
    task_service: Annotated[
        TaskService, Depends(get_tasks_service)
    ],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    try:
        task = await task_service.update_task(
            task_id=task_id,
            task_update=task_update,
            user_id=user_id,
        )
    except TaskNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error.message,
        )
    return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(
    task_id: int,
    task_service: Annotated[
        TaskService, Depends(get_tasks_service)
    ],
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> None:
    try:
        await task_service.delete_task(
            task_id=task_id,
            user_id=user_id,
        )
    except TaskNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error.message,
        )
