from exceptions import TaskNotFoundError
from repository import TaskCache, TaskRepository
from schemas import TaskCreateSchema, TaskSchema


class TaskService:
    def __init__(
        self,
        task_repository: TaskRepository,
        task_cache: TaskCache,
    ) -> None:
        self.task_repository = task_repository
        self.task_cache = task_cache

    def get_tasks(
        self,
        user_id: int,
    ) -> list[TaskSchema]:
        # if not (
        #     tasks_schema := self.task_cache.get_tasks()
        # ):
        tasks_model = self.task_repository.get_tasks(
            user_id=user_id
        )
        tasks_schema = [
            TaskSchema.model_validate(task_model)
            for task_model in tasks_model
        ]
        # if tasks_schema:
        #     self.task_cache.set_tasks(tasks_schema)
        return tasks_schema

    def get_task_by_id(
        self,
        task_id: int,
        user_id: int,
    ) -> TaskSchema:
        task_model = self.task_repository.get_task_by_id(
            task_id=task_id,
            user_id=user_id,
        )
        if not task_model:
            raise TaskNotFoundError
        return TaskSchema.model_validate(task_model)

    def create_task(
        self, task_in: TaskCreateSchema, user_id: int
    ) -> TaskSchema:
        task_model = self.task_repository.create_task(
            task_in=task_in,
            user_id=user_id,
        )
        task = TaskSchema.model_validate(task_model)
        return task

    def update_task(
        self,
        task_id: int,
        task_update: TaskCreateSchema,
        user_id: int,
    ) -> TaskSchema:
        if not self._validate_user_task(
            task_id=task_id,
            user_id=user_id,
        ):
            raise TaskNotFoundError
        task_model = self.task_repository.update_task(
            task_id=task_id,
            task_update=task_update,
            user_id=user_id,
        )
        task = TaskSchema.model_validate(task_model)
        return task

    def delete_task(
        self, task_id: int, user_id: int
    ) -> None:
        if not self._validate_user_task(
            task_id=task_id,
            user_id=user_id,
        ):
            raise TaskNotFoundError
        self.task_repository.delete_task(
            task_id=task_id,
            user_id=user_id,
        )

    def _validate_user_task(
        self, task_id: int, user_id: int
    ) -> bool:
        return bool(
            self.task_repository.get_task_by_id(
                task_id=task_id,
                user_id=user_id,
            )
        )
