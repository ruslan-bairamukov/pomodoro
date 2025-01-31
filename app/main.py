from typing import Annotated

from fastapi import Depends, FastAPI

from app.dependencies import get_tasks_repository
from app.tasks.handlers import router as tasks_router
from app.tasks.repository.task_repo import TaskRepository
from app.users.auth.handlers import router as auth_router
from app.users.user_profile.handlers import (
    router as user_profile_handler,
)

app = FastAPI()
app.include_router(router=tasks_router)
app.include_router(router=user_profile_handler)
app.include_router(router=auth_router)


@app.get("/app/ping")
async def ping_app():
    return {"message": "app is working"}


@app.get("/db/ping")
async def ping_db(
    task_repository: Annotated[
        TaskRepository, Depends(get_tasks_repository)
    ],
):
    return await task_repository.ping_db()
