from repository import UserRepository
from schemas import UserInSchema, UserOutSchema


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository,
    ) -> None:
        self.user_repository = user_repository

    def login(
        self,
        user_in: UserInSchema,
    ) -> UserOutSchema | None:
        user_profile = (
            self.user_repository.get_user_by_username(
                username=user_in.username,
            )
        )
        if self.user_repository._validate_auth_user(
            user_profile=user_profile,
            password=user_in.password,
        ):
            return UserOutSchema.model_validate(
                user_profile
            )
