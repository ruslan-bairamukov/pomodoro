from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from cryptography.hazmat.primitives import serialization
from cryptography.x509 import load_pem_x509_certificate
from pydantic import computed_field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

BASE_DIR: Path = Path(__file__).resolve().parent.parent
BASE_MODEL_CONFIG = SettingsConfigDict(
    env_file=BASE_DIR / ".local.env",
    env_file_encoding="utf-8",
    extra="ignore",
)


class SQLITEDbSettings(BaseSettings):
    model_config = BASE_MODEL_CONFIG

    SQLITE_DIALECT: str
    SQLITE_DRIVER: str
    ECHO: bool
    SQLITE_PATH: Path = BASE_DIR / "pomodoro.db"

    @property
    def url(self) -> str:
        return f"{self.SQLITE_DIALECT}+{self.SQLITE_DRIVER}:///{self.SQLITE_PATH}"


class PSQLDbSettings(BaseSettings):
    model_config = BASE_MODEL_CONFIG

    PSQL_ASYNC_DRIVER: str
    PSQL_DIALECT: str
    PSQL_DRIVER: str
    PSQL_ECHO: bool
    PSQL_HOST: str
    PSQL_NAME: str
    PSQL_PORT: int
    PSQL_USER: str
    PSQL_USER_PASSWORD: str

    @property
    def url(self) -> str:
        return f"{self.PSQL_DIALECT}+{self.PSQL_ASYNC_DRIVER}://{self.PSQL_USER}:{self.PSQL_USER_PASSWORD}@{self.PSQL_HOST}:{self.PSQL_PORT}/{self.PSQL_NAME}"


class RedisSettings(BaseSettings):
    model_config = BASE_MODEL_CONFIG

    REDIS_HOST: str
    REDIS_PORT: int
    # REDIS_DB: int
    # REDIS_USERNAME: str
    # REDIS_USER_PASSWORD: SecretStr

    @property
    def url(self) -> str:
        return (
            f"redis://@{self.REDIS_HOST}:{self.REDIS_PORT}"
        )


class AuthJWT(BaseSettings):
    model_config = BASE_MODEL_CONFIG

    ISSUER: str
    SUBJECT: str | None = None
    AUDIENCE: str
    EXPIRE_DELTA: timedelta = timedelta(minutes=30)
    SCOPE: str
    ALGORITHM: str
    TOKEN_TYPE: str
    KID: str

    @computed_field
    @property
    def payload(self) -> dict[str, Any]:
        iat = datetime.now(tz=timezone.utc)
        return {
            "iss": self.ISSUER,
            "sub": self.SUBJECT,
            "aud": self.AUDIENCE,
            "iat": iat,
            "exp": iat + self.EXPIRE_DELTA,
            "scope": self.SCOPE,
        }

    @computed_field
    @property
    def headers(self) -> dict[str, Any]:
        return {
            "alg": self.ALGORITHM,
            "typ": self.TOKEN_TYPE,
            "kid": self.KID,
        }

    @computed_field
    @property
    def private_key(
        self,
        keypath: str = ".certs/private_key.pem",
    ) -> str:
        private_key_text = (BASE_DIR / keypath).read_text()
        return serialization.load_pem_private_key(
            private_key_text.encode(encoding="utf-8"),
            password=None,
        )

    @computed_field
    @property
    def public_key(
        self,
        keypath: str = ".certs/public_key.pem",
    ) -> str:
        public_key_text = (BASE_DIR / keypath).read_text()
        return load_pem_x509_certificate(
            public_key_text.encode("utf-8")
        ).public_key()


class GoogleOIDC(BaseSettings):
    model_config = BASE_MODEL_CONFIG

    GOOGLE_CLIENT_ID: str
    PROJECT_ID: str
    GOOGLE_AUT_URI: str
    GOOGLE_TOKEN_URI: str
    GOOGLE_TOKEN_URL: str
    AUTH_PROVIDER_X509_CERT_URL: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str

    @computed_field
    @property
    def google_redirect_url(self) -> str:
        return f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={self.GOOGLE_CLIENT_ID}&redirect_uri={self.GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"


class YandexOIDC(BaseSettings):
    model_config = BASE_MODEL_CONFIG

    YANDEX_CLIENT_ID: str
    YANDEX_CLIENT_SECRET: str
    YANDEX_TOKEN_URL: str
    YANDEX_REDIRECT_URI: str

    @computed_field
    @property
    def yandex_redirect_url(self) -> str:
        return f"https://oauth.yandex.ru/authorize?response_type=code&client_id={self.YANDEX_CLIENT_ID}&force_confirm=yes"


class Settings(BaseSettings):
    model_config = BASE_MODEL_CONFIG

    AUTH_JWT: AuthJWT = AuthJWT()
    PSQL_DB: PSQLDbSettings = PSQLDbSettings()
    SQLITEDB: SQLITEDbSettings = SQLITEDbSettings()
    REDIS: RedisSettings = RedisSettings()
    GOOGLE_OIDC: GoogleOIDC = GoogleOIDC()
    YANDEX_OIDC: YandexOIDC = YandexOIDC()


settings = Settings()
