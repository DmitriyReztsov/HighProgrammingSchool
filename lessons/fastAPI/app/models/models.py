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
