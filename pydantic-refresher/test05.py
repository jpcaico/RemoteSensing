# computed fields

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
    model_validator,
    computed_field
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
    first_name: str = ""
    last_name: str = ""
    follower_count: int = 0
    is_active: bool = True
 

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
            return f"https://{v}"
        return v
    
    @computed_field
    @property
    def display_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    @computed_field
    @property
    def is_influencer(self) -> bool:
        return self.follower_count > 1000
    
# model validator

class UserRegistration(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str

    @model_validator(mode="after")
    def password_match(self) -> "UserRegistration":
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self
    

# try:
#     registration = UserRegistration(
#         email="joao@gmail.com",
#         password="secret123",
#         confirm_password="secret456"
#     )
# except ValidationError as e:
#     print(e)




user = User(
    username="Joao_Paulo",
    email="Joao@gmail.com",
    age=29,
    password="secret!23",
    #error, does not start with http or https
    website="jp.com",
    first_name="JP",
    last_name="Alvim",
    follower_count=10000
)

print(user.model_dump_json(indent=2))
    


