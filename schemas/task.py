from pydantic import BaseModel, ConfigDict


class TaskCreateSchema(BaseModel):
    name: str | None = None
    pomodoro_count: int | None = None
    category_id: int | None = None

    model_config = ConfigDict(
        from_attributes=True,
    )


class TaskSchema(TaskCreateSchema):
    id: int
    user_id: int
