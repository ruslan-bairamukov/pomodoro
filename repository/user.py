from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import UserProfile
from schemas import UserProfileSchema


class UserRepository:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def create_user(
        self, user_profile: UserProfileSchema
    ) -> UserProfile:
        user_profile_model = UserProfile(
            **user_profile.model_dump()
        )
        async with self.db_session as session:
            session.add(user_profile_model)
            await session.commit()
            await session.refresh(user_profile_model)
        return user_profile_model

    async def get_user_by_id(
        self, user_id: int
    ) -> UserProfile | None:
        query = select(UserProfile).where(
            UserProfile.id == user_id
        )
        async with self.db_session as session:
            user_profile = await session.execute(query)
        return user_profile.scalar_one_or_none()

    async def get_user_by_email(
        self,
        email: str,
    ) -> UserProfile | None:
        query = select(UserProfile).where(
            UserProfile.email == email
        )
        async with self.db_session as session:
            user_profile = await session.execute(query)
        return user_profile.scalar_one_or_none()

    async def get_user_by_username(
        self,
        username: str,
    ) -> UserProfile | None:
        query = select(UserProfile).where(
            UserProfile.username == username
        )
        async with self.db_session as session:
            user_profile = await session.execute(query)
        return user_profile.scalar_one_or_none()
