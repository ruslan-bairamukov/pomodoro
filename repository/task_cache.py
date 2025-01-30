from redis import Redis

from schemas import TaskSchema


class TaskCache:
    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    async def get_tasks(self) -> list[TaskSchema]:
        async with self.redis as redis:
            tasks_json = await redis.lrange(
                name="tasks",
                start=0,
                end=-1,
            )
        return [
            TaskSchema.model_validate_json(task_json)
            for task_json in tasks_json
        ]

    async def set_tasks(
        self, tasks: list[TaskSchema]
    ) -> None:
        tasks_json = (
            task.model_dump_json() for task in tasks
        )
        """
        TODO add expiration params for data being saved in Redis 
        """
        async with self.redis as redis:
            await redis.lpush("tasks", *tasks_json)
