from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class DbSettings(BaseModel):
    DIALECT: str = "sqlite"
    DRIVER: str = "pysqlite"
    PATH: Path = (
        Path(__file__).resolve().parent.parent
        / "pomodoro.db"
    )
    URL: str = f"{DIALECT}+{DRIVER}:///{PATH}"
    ECHO: bool = True


class AsyncDbSettings(BaseModel):
    DIALECT: str = "postgresql"
    DRIVER: str = "psycopg2"  # "asyncpg"
    URL: str = f"{DIALECT}+{DRIVER}://postgres:superSECRETpassword@192.168.1.84:15432/pomodoro"
    ECHO: bool = False


class RedisSettings(BaseModel):
    HOST: str = "192.168.1.84"
    PORT: int = 36379
    DB: int = 0
    PASSWORD: str = ""
    USERNAME: str = "default"
    URL: str = (
        f"redis://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB}"
    )


class AuthJWT(BaseModel):
    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"


class Settings(BaseSettings):
    GOOGLE_TOKEN_ID: str = "2803463467272300832"
    ASYNC_DB: AsyncDbSettings = AsyncDbSettings()
    AUTH_JWT: AuthJWT = AuthJWT()
    DB: DbSettings = DbSettings()
    REDIS: RedisSettings = RedisSettings()

    model_config = SettingsConfigDict(env_file=".dev.env")


settings = Settings()


# class DbSettings(BaseModel):
#     DIALECT: str = "sqlite"
#     DRIVER: str = "pysqlite"
#     PATH: Path = Path(__file__).resolve().parent.parent / "pomodoro.db"
#     URL: str = f"{DIALECT}+{DRIVER}:///{PATH}"
#     ECHO: bool = True
