from sqlalchemy.orm import DeclarativeMeta, Mapped, mapped_column


class Tasks(DeclarativeMeta):
    __tablename__ = "Tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    pomodoro_count: Mapped[int]
    category_id: Mapped[int]