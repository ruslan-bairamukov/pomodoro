from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class PomodoroCount(Base):
    __tablename__ = "pomodoro_count"
