from datetime import timedelta
from typing import Any

import jwt
from passlib.context import CryptContext

from app.config import Settings, settings
from app.exceptions import (
    IncorrectPasswordError,
    UserNotFoundError,
)
from app.users.auth.clients.google import GoogleClient
from app.users.auth.clients.yandex import YandexClient
from app.users.auth.schemas import UserLoginSchema
from app.users.user_profile.models import UserProfile
from app.users.user_profile.repository import UserRepository
from app.users.user_profile.schemas import UserProfileSchema


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository,
        settings: Settings = settings,
    ) -> None:
        self.user_repository = user_repository
        self.settings = settings
        self.password_context: CryptContext = CryptContext(
            schemes=["bcrypt"],
            deprecated="auto",
        )

    async def password_login(
        self,
        username: str,
        password: str,
    ) -> UserLoginSchema | None:
        user_profile = (
            await self.user_repository.get_user_by_username(
                username=username,
            )
        )
        await self._validate_user(
            password=password,
            user_profile=user_profile,
        )
        access_token = await self.generate_jwt(
            user_id=user_profile.id
        )
        return UserLoginSchema(
            id=user_profile.id,
            access_token=access_token,
        )

    async def oidc_login(
        self,
        code: str,
        oidc_client: GoogleClient | YandexClient,
    ):
        user_data = await oidc_client.get_user_info(
            code=code
        )
        if not (
            user_profile_model
            := await self.user_repository.get_user_by_email(
                email=user_data.email
            )
        ):
            user_profile = UserProfileSchema(
                **user_data.model_dump()
            )
            user_profile_model = (
                await self.user_repository.create_user(
                    user_profile=user_profile
                )
            )
        access_token = await self.generate_jwt(
            user_id=user_profile_model.id
        )
        return UserLoginSchema(
            id=user_profile_model.id,
            access_token=access_token,
        )

    async def get_google_redirect_url(self) -> str:
        return self.settings.GOOGLE_OIDC.google_redirect_url

    async def get_yandex_redirect_url(self) -> str:
        return self.settings.YANDEX_OIDC.yandex_redirect_url

    async def generate_jwt(
        self,
        user_id: int,
    ) -> jwt.PyJWT:
        payload = self.settings.AUTH_JWT.payload.copy()
        payload.update({"sub": str(user_id)})
        return jwt.encode(
            payload=payload,
            key=self.settings.AUTH_JWT.private_key,
            algorithm=self.settings.AUTH_JWT.ALGORITHM,
            headers=self.settings.AUTH_JWT.headers,
        )

    async def validate_jwt(
        self, token: str
    ) -> dict[str, Any]:
        """
        Validates an access token. If the token is valid, it returns the token payload.
        """
        return jwt.decode(
            jwt=token,
            key=self.settings.AUTH_JWT.public_key,
            algorithms=[
                self.settings.AUTH_JWT.ALGORITHM,
            ],
            audience=self.settings.AUTH_JWT.AUDIENCE,
            issuer=self.settings.AUTH_JWT.ISSUER,
            subject=self.settings.AUTH_JWT.SUBJECT,
            leeway=timedelta(minutes=5),
        )

    async def _validate_user(
        self,
        password: str,
        user_profile: UserProfile,
    ) -> None:
        if not user_profile:
            raise UserNotFoundError
        if not await self._verify_password(
            plain_password=password,
            hashed_password=user_profile.hashed_password,
        ):
            raise IncorrectPasswordError

    async def _verify_password(
        self,
        plain_password: str,
        hashed_password: str,
    ) -> bool:
        return await self.password_context.verify(
            secret=plain_password,
            hash=hashed_password,
        )
