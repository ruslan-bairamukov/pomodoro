from pydantic import BaseModel, ConfigDict, model_validator


class Task(BaseModel):
    id: int
    name: str
    pomodoro_count: int
    category_id: int

    model_config = ConfigDict(
        from_attributes=True,
    )


class Params(BaseModel):
    name: str | None = None
    pomodoro_count: int | None = None
    category_id: int | None = None

    @model_validator(mode="after")
    def is_name_or_pomodoro_count_not_none(self):
        if self.name is None and self.pomodoro_count is None:
            raise ValueError("name or pomodoro_count must be provided")
        return self
