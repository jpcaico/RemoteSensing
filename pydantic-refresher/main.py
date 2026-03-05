from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
    age: str


user1 = User(username="jp", email="jp@gmail.com", age=29)
print(user1)

user2 = User(username="tj", email=None, age="old")
print(user2)

