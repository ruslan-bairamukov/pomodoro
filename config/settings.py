from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    GOOGLE_TOKEN_ID: str = "2803463467272300832"
    sqlite_db_name: str = "pomodoro.db"

    model_config = SettingsConfigDict(env_file=".dev.env")


settings = Settings()