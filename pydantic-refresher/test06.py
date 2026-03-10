# nested models

# computed fields

# Decorators
from typing import Annotated, Literal
from uuid import UUID, uuid4
from functools import partial
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
    

class Comment(BaseModel):
    content: str
    author_email: EmailStr
    likes: int = 0

class BlogPost(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=200)]
    content: Annotated[str, Field(min_length=10)]
    author: User # nested - full object
    view_count: int = 0
    is_published: bool = False
    tags: list[str] = Field(default_factory=list) # everytime we create a user, it calls List to create a fresh empty list for each user
    slug: Annotated[str, Field(pattern=r"^[a-z0-9-]+$")]
    created_at : datetime = Field(default_factory=partial(datetime.now, tz=UTC)) #partial is going to return an unexecuted function that is the datetime.now with tz=UTC ready to go
    status: Literal["draft", "published", "archived"] = "draft" 
    comments: list[Comment] = Field(default_factory=list)
    
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


post_data = {
    "title" : "My First Blog Post",
    "content" : "This is the content of my first blog post. It has more than 10 characters.",
    "slug" : "my-first-blog-post",
    "author" : {
        "username" : "Joao_Paulo",
        "email" : "joao@gmail.com",
        "age" : 29,
        "password" : "secret!23",
    },
    "comments": [
        {
            "content": "Great post!",
            "author_email": "joao@gmail.com",
            "likes": 10
        },
        {
            "content": "Thanks for sharing.",
            "author_email": "joao@gmail.com",
            "likes": 5
        }
    ]
}

post = BlogPost(**post_data)
print(post.model_dump_json(indent=2))

# user = User(
#     username="Joao_Paulo",
#     email="Joao@gmail.com",
#     age=29,
#     password="secret!23",
#     #error, does not start with http or https
#     website="jp.com",
#     first_name="JP",
#     last_name="Alvim",
#     follower_count=10000
# )

# print(user.model_dump_json(indent=2))
    


