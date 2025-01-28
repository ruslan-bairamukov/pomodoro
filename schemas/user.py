from pydantic import BaseModel, ConfigDict


class UserInSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    password: str


class UserProfileSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    username: str
    hashed_password: str


class UserLoginSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    access_token: str
