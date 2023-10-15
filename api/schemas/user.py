import time

from pydantic import BaseModel, Field

from api.schemas.common import PER_PAGE, ObjectIDModel


class CreateUser(BaseModel):
    login: str = Field(min_length=5, max_length=30)
    password: str = Field(min_length=8, max_length=30)
    name: str = Field(..., min_length=5, max_length=30)
    is_superuser: bool = Field(False)
    created: int | float = int(time.time())


class CreateUserResponse(BaseModel):
    new_user: str


class User(CreateUser, ObjectIDModel):
    pass


class UserResponse(BaseModel):
    page: int = 1
    limit: int = PER_PAGE
    result: list[User]
