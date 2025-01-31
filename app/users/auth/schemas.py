from pydantic import BaseModel, ConfigDict, Field


class GoogleUserData(BaseModel):
    sub: int
    email: str
    email_verified: bool
    name: str
    google_access_token: str


class YandexUserData(BaseModel):
    sub: int = Field(alias="id")
    login: str
    name: str = Field(alias="real_name")
    email: str = Field(alias="default_email")
    yandex_access_token: str


class UserLoginSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    access_token: str
