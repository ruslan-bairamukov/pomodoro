from sqlalchemy import and_, delete, select, update
from sqlalchemy.orm import Session

from models import Categories, Tasks
from schemas import TaskCreateSchema


class TaskRepository:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def get_tasks(
        self,
        user_id: int,
    ) -> list[Tasks] | None:
        query = select(Tasks).where(
            Tasks.user_id == user_id
        )
        with self.db_session as session:
            tasks = session.execute(query).scalars().all()
        return tasks

    def get_task_by_id(
        self,
        task_id: int,
        user_id: int,
    ) -> Tasks | None:
        query = select(Tasks).where(
            and_(
                Tasks.id == task_id,
                Tasks.user_id == user_id,
            )
        )
        with self.db_session as session:
            response = session.execute(
                query
            ).scalar_one_or_none()
        return response

    def get_tasks_by_category_name(
        self,
        category_name: str,
        user_id: int,
    ) -> list[Tasks] | None:
        query = (
            select(Tasks)
            .join(
                Categories,
                onclause=Tasks.category_id == Categories.id,
            )
            .where(
                and_(
                    Categories.name == category_name,
                    Tasks.user_id == user_id,
                )
            )
        )
        with self.db_session as session:
            tasks = session.execute(query).scalars().all()
        return tasks

    def create_task(
        self,
        task_in: TaskCreateSchema,
        user_id: int,
    ) -> Tasks:
        task_model = Tasks(
            **task_in.model_dump(),
            user_id=user_id,
        )
        with self.db_session as session:
            session.add(task_model)
            session.commit()
            session.refresh(task_model)
        return task_model

    def update_task(
        self,
        task_id: int,
        task_update: TaskCreateSchema,
        user_id: int,
    ) -> Tasks:
        query = (
            update(Tasks)
            .where(
                and_(
                    Tasks.id == task_id,
                    Tasks.user_id == user_id,
                )
            )
            .values(
                **task_update.model_dump(exclude_unset=True)
            )
        )
        with self.db_session as session:
            session.execute(query)
            session.commit()
        task_model = self.get_task_by_id(
            task_id=task_id,
            user_id=user_id,
        )
        return task_model

    def delete_task(
        self,
        task_id: int,
        user_id: int,
    ) -> None:
        query = delete(Tasks).where(
            and_(
                Tasks.id == task_id,
                Tasks.user_id == user_id,
            )
        )
        with self.db_session as session:
            session.execute(query)
            session.commit()
