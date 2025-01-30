from passlib.context import CryptContext

from repository import UserRepository
from schemas import (
    UserCreateSchema,
    UserLoginSchema,
    UserProfileSchema,
)
from service import AuthService


class UserService:
    def __init__(
        self,
        user_repository: UserRepository,
        auth_service: AuthService,
    ) -> None:
        self.user_repository = user_repository
        self.auth_service = auth_service
        self.password_context: CryptContext = CryptContext(
            schemes=["bcrypt"],
            deprecated="auto",
        )

    async def create_user(
        self,
        user_in: UserCreateSchema,
    ) -> UserLoginSchema:
        user_profile = await self._create_user_profile(
            user_in=user_in
        )
        user_profile_model = (
            await self.user_repository.create_user(
                user_profile=user_profile,
            )
        )
        access_token = await self.auth_service.generate_jwt(
            user_id=user_profile_model.id
        )
        return UserLoginSchema(
            id=user_profile_model.id,
            access_token=access_token,
        )

    async def _create_user_profile(
        self,
        user_in: UserCreateSchema,
    ) -> UserProfileSchema:
        hashed_password = await self._get_password_hash(
            password=user_in.password
        )
        return UserProfileSchema(
            **user_in.model_dump(
                exclude=UserCreateSchema.password,
                exclude_none=True,
            ),
            hashed_password=hashed_password,
        )

    async def _get_password_hash(
        self, password: str | bytes
    ) -> str:
        return await self.password_context.hash(password)
