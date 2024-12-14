from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    GOOGLE_TOKEN_ID: str = "2803463467272300832"

    model_config = SettingsConfigDict(env_file=".dev.env")


settings = Settings()