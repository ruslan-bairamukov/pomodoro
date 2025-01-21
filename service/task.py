from repository import TaskCache, TaskRepository
from schemas import TaskSchema


class TaskService:
    def __init__(
        self,
        task_repository: TaskRepository,
        task_cache: TaskCache,
    ) -> None:
        self.task_repository = task_repository
        self.task_cache = task_cache

    def get_tasks(self) -> list[TaskSchema]:
        if not (
            tasks_schema := self.task_cache.get_tasks()
        ):
            tasks_model = self.task_repository.get_tasks()
            tasks_schema = [
                TaskSchema.model_validate(task_model)
                for task_model in tasks_model
            ]
            if tasks_schema:
                self.task_cache.set_tasks(tasks_schema)
        return tasks_schema
