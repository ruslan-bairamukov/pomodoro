from pydantic import BaseModel, ConfigDict


class UserInSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    password: str


class UserProfileSchema(UserInSchema):
    id: int | None = None
    access_token: str | None = None


class UserOutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    access_token: str
