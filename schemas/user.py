from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str | None = None
    name: str | None = None


class UserCreateSchema(UserSchema):
    username: str
    password: str


class UserProfileSchema(UserSchema):
    id: int | None = None
    username: str | None = None
    hashed_password: str | None = None
    google_access_token: str | None = None
    yandex_access_token: str | None = None
