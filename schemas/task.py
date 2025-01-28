from pydantic import BaseModel, ConfigDict, model_validator


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


class ParamsSchema(BaseModel):
    name: str | None = None
    pomodoro_count: int | None = None
    category_id: int | None = None

    @model_validator(mode="after")
    def is_name_or_pomodoro_count_not_none(self):
        if (
            self.name is None
            and self.pomodoro_count is None
        ):
            raise ValueError(
                "name or pomodoro_count must be provided"
            )
        return self
