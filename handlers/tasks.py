from fastapi import APIRouter, Depends, status
from typing import Annotated

from schemas.task import Task, Params
from dependencies.fake_data import fake_tasks
from dependencies.util import find_task_by_id


router = APIRouter(
    prefix="/tasks",
    tags=["task"],
)


@router.get(
    "/all",
    response_model=list[Task],
    status_code=status.HTTP_200_OK,
)
async def get_tasks(
    tasks: Annotated[dict[int, Task], Depends(fake_tasks)],
):
    return [task for task in tasks.values()]


@router.get("/{task_id}")
async def get_task_by_id(
    task: Annotated[Task, Depends(find_task_by_id)],
):
    return {"task": task}


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    params: Params,
    tasks: Annotated[dict[int, Task], Depends(fake_tasks)],
):
    task_id = max(tasks, default=0) + 1
    task = Task(id=task_id, **params.model_dump())
    tasks[task_id] = task
    return {"message": f"'{task}' task has been created"}


@router.patch("/{task_id}")
async def update_task(
    params: Params,
    task: Annotated[Task, Depends(find_task_by_id)],
):
    task.__dict__.update(**params.model_dump(exclude_none=True))
    return {"task": task}


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(
    task: Annotated[Task, Depends(find_task_by_id)],
    tasks: Annotated[dict[int, Task], Depends(fake_tasks)],
):
    tasks.pop(task.id)
    return {"task": task}
