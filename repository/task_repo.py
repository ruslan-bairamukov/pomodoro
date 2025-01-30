from fastapi import HTTPException, status
from sqlalchemy import and_, delete, select, text, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models import Categories, Tasks
from schemas import TaskCreateSchema


class TaskRepository:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def ping_db(self) -> dict[str, str]:
        async with self.db_session as session:
            try:
                await session.execute(text("select 1"))
            except IntegrityError:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Database is unavailable",
                )
            return {"message": "db is working"}

    async def get_tasks(
        self,
        user_id: int,
    ) -> list[Tasks] | None:
        query = select(Tasks).where(
            Tasks.user_id == user_id
        )
        async with self.db_session as session:
            tasks = await session.execute(query)
        return tasks.scalars().all()

    async def get_task_by_id(
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
        async with self.db_session as session:
            response = await session.execute(query)
        return response.scalar_one_or_none()

    async def get_tasks_by_category_name(
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
        async with self.db_session as session:
            tasks = await session.execute(query)
        return tasks.scalars().all()

    async def create_task(
        self,
        task_in: TaskCreateSchema,
        user_id: int,
    ) -> Tasks:
        task_model = Tasks(
            **task_in.model_dump(),
            user_id=user_id,
        )
        async with self.db_session as session:
            session.add(task_model)
            await session.commit()
            await session.refresh(task_model)
        return task_model

    async def update_task(
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
        async with self.db_session as session:
            await session.execute(query)
            await session.commit()
        task_model = await self.get_task_by_id(
            task_id=task_id,
            user_id=user_id,
        )
        return task_model

    async def delete_task(
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
        async with self.db_session as session:
            await session.execute(query)
            await session.commit()
