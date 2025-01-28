from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class Tasks(Base):
    __tablename__ = "tasks"

    name: Mapped[str]
    pomodoro_count: Mapped[int]
    category_id: Mapped[int] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user_profile.id"),
        nullable=False,
    )
