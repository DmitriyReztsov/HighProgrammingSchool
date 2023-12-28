from typing import Optional

from pydantic import BaseModel, EmailStr, conint, constr


# создаём модель данных, которая обычно расположена в файле models.py
class User(BaseModel):
    username: str
    age: conint(gt=18)
    email: EmailStr
    password: constr(min_length=8, max_length=16)
    phone: Optional[str] = "Unknown"


class TodoCreate(BaseModel):
    title: str
    description: str
    completed: bool = False


class TodoRetrieve(BaseModel):
    id: int
    title: str
    description: str
    completed: bool = False


class TodoUpdate(BaseModel):
    title: str = None
    description: str = None
    completed: bool = None
