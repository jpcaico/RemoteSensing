from pydantic import BaseModel, ValidationError
from datetime import datetime

class User(BaseModel):
    uid: int
    username: str
    email: str

    verified_at: datetime | None = None

    bio: str = ""
    is_active: bool = True

    full_name: str | None = None

try:
    user = User(
        uid="123", #pydantic has type conversion enabled by default
        username = None,
        email = 123
    )
except ValidationError as e:
    print(e)

#changing fields after creation does not trigger revalidation
user.bio = 123

user.bio = "Python Dev"

print(user.bio)

#useful when you need to serialize your models for storage or sending over a network
print(user.model_dump())
print(user.model_dump_json(indent=2))

