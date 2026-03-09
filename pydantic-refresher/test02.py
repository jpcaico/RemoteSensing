#annotated
from pydantic import BaseModel, ValidationError, Field
from functools import partial
from datetime import datetime, UTC
from typing import Literal, Annotated

class User(BaseModel):
    uid: Annotated[int, Field(gt=0)]
    username: Annotated[str, Field(min_length=3, max_length=20)]
    age: Annotated[int, Field(ge=13, le=130)]
    email: str

    verified_at: datetime | None = None

    bio: str = ""
    is_active: bool = True

    full_name: str | None = None


class BlogPost(BaseModel):
    author_id: str | int
    title: Annotated[str, Field(min_length=1, max_length=200)]
    content: Annotated[str, Field(min_length=10)]
    view_count: int = 0
    is_published: bool = False
    tags: list[str] = Field(default_factory=list) # everytime we create a user, it calls List to create a fresh empty list for each user
    slug: Annotated[str, Field(pattern=r"^[a-z0-9-]+$")]

    # created_at: datetime = datetime.now(UTC) #this would call datetime.now once when the class is defined, not when each instance is created. every post will have the same timestamp

    #solution #1
    #created_at: datetime = Field(default_factory = lambda: datetime.now(tz=UTC))

    #solution 2
    created_at : datetime = Field(default_factory=partial(datetime.now, tz=UTC)) #partial is going to return an unexecuted function that is the datetime.now with tz=UTC ready to g
    status: Literal["draft", "published", "archived"] = "draft"
    

## Invalid User
try:
    user = User(
        uid=0,
        username="cs",
        email="email@gmail.com",
        age=12
    )
except ValidationError as e:
    print(e)




# New Blog Post

# post = BlogPost(
#     title="Refreshing Pydantic",
#     content="Here it is",
#     author_id="12345"
# )

# print(post)