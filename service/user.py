import random
import string

from repository import UserRepository
from schemas import (
    UserInSchema,
    UserOutSchema,
    UserProfileSchema,
)


class UserService:
    def __init__(
        self,
        user_repository: UserRepository,
    ) -> None:
        self.user_repository = user_repository

    def create_user(
        self,
        user_in: UserInSchema,
    ) -> UserOutSchema:
        access_token = self._generate_access_token()
        user_profile = UserProfileSchema(
            username=user_in.username,
            password=user_in.password,
            access_token=access_token,
        )
        user_profile_model = (
            self.user_repository.create_user(
                user_profile=user_profile,
            )
        )
        return UserOutSchema.model_validate(
            user_profile_model
        )

    def _generate_access_token(self) -> str:
        str_sequence = (
            string.ascii_uppercase
            + string.digits
            + string.printable
        )
        return "".join(
            random.choice(str_sequence) for _ in range(21)
        )
