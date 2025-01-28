from sqlalchemy import select
from sqlalchemy.orm import Session

from models import UserProfile
from schemas import UserProfileSchema


class UserRepository:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def create_user(
        self, user_profile: UserProfileSchema
    ) -> UserProfile:
        user_profile_model = UserProfile(
            **user_profile.model_dump()
        )
        with self.db_session as session:
            session.add(user_profile_model)
            session.commit()
            session.refresh(user_profile_model)
        return user_profile_model

    def get_user_by_id(
        self, user_id: int
    ) -> UserProfile | None:
        query = select(UserProfile).where(
            UserProfile.id == user_id
        )
        with self.db_session as session:
            user_profile = session.execute(
                query
            ).scalar_one_or_none()
        return user_profile

    def get_user_by_username(
        self,
        username: str,
    ) -> UserProfile | None:
        query = select(UserProfile).where(
            UserProfile.username == username
        )
        with self.db_session as session:
            user_profile = session.execute(
                query
            ).scalar_one_or_none()
        return user_profile
