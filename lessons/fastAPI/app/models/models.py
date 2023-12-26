from typing import Optional

from pydantic import BaseModel


# создаём модель данных, которая обычно расположена в файле models.py
class User(BaseModel):
    id: int = 0
    name: str
    token: str = None
    user_info: str
    age: int = 0


class AuthUser(BaseModel):
    username: str
    password: str


class Feedback(BaseModel):
    name: str
    message: str


class Product(BaseModel):
    product_id: int
    name: str
    category: str
    price: float


# SQLite async
# Модель User для валидации входных данных
class UserCreate(BaseModel):
    username: str
    email: str


# Модель User для валидации исходящих данных
class UserReturn(BaseModel):
    username: str
    email: str
    id: Optional[int] = None


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
