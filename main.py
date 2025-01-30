from typing import Annotated

from fastapi import Depends, FastAPI

from dependencies import get_tasks_repository
from handlers import routers
from repository import TaskRepository

app = FastAPI()
for router in routers:
    app.include_router(router=router)


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
