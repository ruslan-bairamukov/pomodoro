from fastapi import Depends, HTTPException, status
from typing import Annotated

from dependencies.fake_data import fake_tasks
from schemas.task import Task


def find_task_by_id(
    task_id: int,
    tasks: Annotated[dict[int, Task], Depends(fake_tasks)],
) -> Task:
    try:
        return tasks[task_id]
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not found task with {task_id = }",
        )
