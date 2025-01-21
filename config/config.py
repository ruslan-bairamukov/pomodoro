from pathlib import Path

from pydantic import SecretStr
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
        return f"{self.PSQL_DIALECT}+{self.PSQL_DRIVER}://{self.PSQL_USER}:{self.PSQL_USER_PASSWORD}@{self.PSQL_HOST}:{self.PSQL_PORT}/{self.PSQL_NAME}"


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

    SECRET_KEY: SecretStr
    ALGORITHM: str


class Settings(BaseSettings):
    model_config = BASE_MODEL_CONFIG

    GOOGLE_TOKEN_ID: SecretStr
    AUTH_JWT: AuthJWT = AuthJWT()
    PSQL_DB: PSQLDbSettings = PSQLDbSettings()
    SQLITEDB: SQLITEDbSettings = SQLITEDbSettings()
    REDIS: RedisSettings = RedisSettings()


settings = Settings()
