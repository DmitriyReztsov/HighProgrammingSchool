from typing import Optional

from pydantic import BaseModel, EmailStr, conint, constr, validator


# создаём модель данных, которая обычно расположена в файле models.py
class User(BaseModel):
    username: Optional[str] = None
    first_name: str
    last_name: str
    age: conint(gt=18)
    email: EmailStr
    password: constr(min_length=8, max_length=16)
    phone: Optional[str] = "Unknown"

    @validator("age")
    @classmethod
    def validate_age(cls, value):
        if value > 100:
            raise ValueError("Столько не живут!")
        return value


class UserRetrieve(BaseModel):
    username: str
    first_name: str
    last_name: str
    age: conint(gt=18)
    email: EmailStr
    phone: str


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
