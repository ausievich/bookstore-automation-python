"""Auth-related Pydantic models."""

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class LoginRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    email: str
    password: str


class UserInfo(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    id: str
    email: str
    name: str


class LoginResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    token: str
    user: UserInfo
