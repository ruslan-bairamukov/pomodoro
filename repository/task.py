from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from data_access import db_helper
from models import Categories, Tasks


class TaskRepository:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def get_tasks(self) -> list[Tasks]:
        with self.db_session as session:
            tasks: list[Tasks] = session.execute(select(Tasks)).scalars().all()
        return tasks

    def get_task_by_id(self, task_id: int) -> Tasks | None:
        query = select(Tasks).where(Tasks.id == task_id)
        with self.db_session as session:
            task = session.execute(query).scalar_one_or_none()
        return task

    def get_tasks_by_category_name(self, category_name: str) -> list[Tasks]:
        query = select(Tasks).join(Categories, onclause=Tasks.category_id == Categories.id).where(Categories.name == category_name)
        with self.db_session as session:
            tasks: list[Tasks] = session.execute(query).scalars().all()
        return tasks

    def create_task(self, task: Tasks) -> None:
        with self.db_session as session:
            session.add(task)
            session.commit()

    def delete_task(self, task_id: int) -> None:
        query = delete(Tasks).where(Tasks.id == task_id)
        with self.db_session as session:
            session.execute(query)
            session.commit()


def get_tasks_repository() -> TaskRepository:
    db_session = db_helper.session_factory()
    return TaskRepository(db_session)
