import os

import databases
from sqlalchemy import Boolean, Column, Integer, String  # create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# строка подключения
if os.getenv("IS_TEST"):
    SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./app/test.db"
else:
    SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./app/sql_app.db"

# для асинхронной Алхимии
database = databases.Database(SQLALCHEMY_DATABASE_URL)

# создаем движок асинхронный SqlAlchemy
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# sync engine and Session
# sync_engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# SessionLocal = sessionmaker(autoflush=False, bind=engine)

# SQLAlchemy models below
Base = declarative_base()


""" to make and apply migrations:
    alembic revision --autogenerate -m "create user table"
    alembic upgrade head

"""


class TodoNewModel(Base):
    __tablename__ = "todonew"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    completed = Column(Boolean, default=False)


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(length=15))
    price = Column(Integer)
    count = Column(Integer)
    description = Column(String(length=150))


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String(length=30), unique=True, index=True)
    password = Column(String)
    age = Column(Integer)
    phone = Column(String(length=12))
    is_active = Column(Boolean, default=True)
