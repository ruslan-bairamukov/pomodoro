from app.exceptions import TaskNotFoundError
from app.tasks.repository.task_cache import TaskCache
from app.tasks.repository.task_repo import TaskRepository
from app.tasks.schemas import TaskCreateSchema, TaskSchema


class TaskService:
    def __init__(
        self,
        task_repository: TaskRepository,
        task_cache: TaskCache,
    ) -> None:
        self.task_repository = task_repository
        self.task_cache = task_cache

    async def get_tasks(
        self,
        user_id: int,
    ) -> list[TaskSchema]:
        # if not (
        #     tasks_schema := self.task_cache.get_tasks()
        # ):
        tasks_model = await self.task_repository.get_tasks(
            user_id=user_id
        )
        tasks_schema = [
            TaskSchema.model_validate(task_model)
            for task_model in tasks_model
        ]
        # if tasks_schema:
        #     self.task_cache.set_tasks(tasks_schema)
        return tasks_schema

    async def get_task_by_id(
        self,
        task_id: int,
        user_id: int,
    ) -> TaskSchema:
        task_model = (
            await self.task_repository.get_task_by_id(
                task_id=task_id,
                user_id=user_id,
            )
        )
        if not task_model:
            raise TaskNotFoundError
        return TaskSchema.model_validate(task_model)

    async def create_task(
        self, task_in: TaskCreateSchema, user_id: int
    ) -> TaskSchema:
        task_model = await self.task_repository.create_task(
            task_in=task_in,
            user_id=user_id,
        )
        task = TaskSchema.model_validate(task_model)
        return task

    async def update_task(
        self,
        task_id: int,
        task_update: TaskCreateSchema,
        user_id: int,
    ) -> TaskSchema:
        if not await self._validate_user_task(
            task_id=task_id,
            user_id=user_id,
        ):
            raise TaskNotFoundError
        task_model = await self.task_repository.update_task(
            task_id=task_id,
            task_update=task_update,
            user_id=user_id,
        )
        task = TaskSchema.model_validate(task_model)
        return task

    async def delete_task(
        self, task_id: int, user_id: int
    ) -> None:
        if not await self._validate_user_task(
            task_id=task_id,
            user_id=user_id,
        ):
            raise TaskNotFoundError
        await self.task_repository.delete_task(
            task_id=task_id,
            user_id=user_id,
        )

    async def _validate_user_task(
        self, task_id: int, user_id: int
    ) -> bool:
        return bool(
            await self.task_repository.get_task_by_id(
                task_id=task_id,
                user_id=user_id,
            )
        )
