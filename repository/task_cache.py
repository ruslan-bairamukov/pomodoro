from redis import Redis

from schemas import TaskSchema


class TaskCache:
    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    def get_tasks(self) -> list[TaskSchema]:
        with self.redis as redis:
            tasks_json = redis.lrange(
                name="tasks",
                start=0,
                end=-1,
            )
        return [
            TaskSchema.model_validate_json(task_json)
            for task_json in tasks_json
        ]

    def set_tasks(self, tasks: list[TaskSchema]) -> None:
        tasks_json = (
            task.model_dump_json() for task in tasks
        )
        """
        TODO add expiration params for data being saved in Redis 
        """
        with self.redis as redis:
            redis.lpush("tasks", *tasks_json)
