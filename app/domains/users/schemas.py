from pydantic import BaseModel, ConfigDict, EmailStr

from app.shared.schemas import FilterPage  # noqa: F401 (reexport conveniente)


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]
