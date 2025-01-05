from fastapi import APIRouter, Depends, status
from typing import Annotated

from schemas.task import Task, Params
from dependencies.fake_data import fake_tasks
from dependencies.util import find_task_by_id
from models.db_helper import get_db_connection


router = APIRouter(
    prefix="/tasks",
    tags=["task"],
)


@router.get(
    "/all",
    response_model=list[Task],
    status_code=status.HTTP_200_OK,
)
async def get_tasks():
    cursor = get_db_connection().cursor()
    query_res = cursor.execute("select * from Tasks;").fetchall()
    tasks = [
        Task(id=task[0], name=task[1], pomodoro_count=task[2], category_id=task[3])
        for task in query_res
    ]
    return tasks


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
    task: Task,
):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "insert into Tasks (name, pomodoro_count, category_id) values(?,?,?)",
        (task.name, task.pomodoro_count, task.category_id),
    )
    conn.commit()
    conn.close()
    return task


@router.patch(
    "/{task_id}",
    response_model=Task,
    status_code=status.HTTP_200_OK,
)
async def update_task(
    task_id: int,
    name: str,
):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "update Tasks set name=? where id=?",
        (name, task_id),
    )
    conn.commit()
    task = cursor.execute("select * from Tasks where id=?", (task_id,)).fetchone()
    conn.close()
    return Task(id=task[0], name=task[1], pomodoro_count=task[2], category_id=task[3])


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(
    task_id: int,
):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "delete from Tasks where id=?",
        (task_id,),
    )
    conn.commit()
    conn.close()
    return {"message": f"task {task_id} deleted successfully"}
