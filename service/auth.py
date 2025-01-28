from datetime import timedelta
from typing import Any

import jwt
from passlib.context import CryptContext

from config import AuthJWT, settings
from exceptions import (
    IncorrectPasswordError,
    UserNotFoundError,
)
from models import UserProfile
from repository import UserRepository
from schemas import UserLoginSchema


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository,
        jwt_data: AuthJWT = settings.AUTH_JWT,
    ) -> None:
        self.user_repository = user_repository
        self.jwt_data = jwt_data
        self.password_context: CryptContext = CryptContext(
            schemes=["bcrypt"],
            deprecated="auto",
        )

    def login_for_access_token(
        self,
        username: str,
        password: str,
    ) -> UserLoginSchema | None:
        user_profile = (
            self.user_repository.get_user_by_username(
                username=username,
            )
        )
        self._validate_user(
            password=password,
            user_profile=user_profile,
        )
        access_token = self.generate_jwt(
            user_id=user_profile.id
        )
        return UserLoginSchema(
            id=user_profile.id,
            access_token=access_token,
        )

    def generate_jwt(
        self,
        user_id: int,
    ) -> jwt.PyJWT:
        payload = self.jwt_data.payload.copy()
        payload.update({"sub": str(user_id)})
        return jwt.encode(
            payload=payload,
            key=self.jwt_data.private_key,
            algorithm=self.jwt_data.ALGORITHM,
            headers=self.jwt_data.headers,
        )

    def validate_jwt(self, token: str) -> dict[str, Any]:
        """
        Validates an access token. If the token is valid, it returns the token payload.
        """
        return jwt.decode(
            jwt=token,
            key=self.jwt_data.public_key,
            algorithms=[self.jwt_data.ALGORITHM],
            audience=self.jwt_data.AUDIENCE,
            issuer=self.jwt_data.ISSUER,
            subject=self.jwt_data.SUBJECT,
            leeway=timedelta(minutes=3),
        )

    def _validate_user(
        self,
        password: str,
        user_profile: UserProfile,
    ) -> None:
        if not user_profile:
            raise UserNotFoundError
        if not self._verify_password(
            plain_password=password,
            hashed_password=user_profile.hashed_password,
        ):
            raise IncorrectPasswordError

    def _verify_password(
        self,
        plain_password: str,
        hashed_password: str,
    ) -> bool:
        return self.password_context.verify(
            secret=plain_password,
            hash=hashed_password,
        )
