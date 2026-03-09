# Decorators
from typing import Annotated, Literal
from uuid import UUID, uuid4
from datetime import datetime, UTC
# 5726
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    HttpUrl,
    SecretStr,
    ValidationError,
    ValidationInfo,
    field_validator,
    model_validator
)

class User(BaseModel):

    uid: UUID = Field(default_factory=uuid4) #new unique id for each user when we create one
    username: Annotated[str, Field(min_length=3, max_length=20)]
    age: Annotated[int, Field(ge=13, le=130)]
    email: EmailStr
    website: HttpUrl | None = None
    password: SecretStr
    verified_at: datetime | None = None
    bio: str = ""
    is_active: bool = True
    full_name: str | None = None

    @field_validator("username")
    @classmethod
    def validate_username(cls, v:str) -> str:
        if not v.replace("_", "").isalnum():
            raise ValueError("Username must be alphanumeric (underscores allowed)")
        return v.lower()
    

    @field_validator("website", mode="before") # we want to run this custom validation before it does the httpsurl validation
    @classmethod
    def add_https(cls, v:str | None) -> str | None:
        if v and not v.startswith(("http://", "https://")):
            return f"https//{v}"
        return v
    


user = User(
    username="Joao_Paulo",
    email="Joao@gmail.com",
    age=29,
    password="secret!23",
    #error, does not start with http or https
    website="jp.com"
)

print(user)