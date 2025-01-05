from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "pomodoro.db"


class DbSettings(BaseModel):
    url: str = f"sqlite:///{DB_PATH}"
    echo: bool = True


class Settings(BaseSettings):
    GOOGLE_TOKEN_ID: str = "2803463467272300832"
    db: DbSettings = DbSettings()

    model_config = SettingsConfigDict(env_file=".dev.env")


settings = Settings()
