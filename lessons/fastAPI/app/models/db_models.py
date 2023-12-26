import databases
from sqlalchemy import Boolean, Column, Integer, String, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# строка подключения
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./HighProgrammingSchool/lessons/fastAPI/app/sql_app.db"  # noqa

# для асинхронной Алхимии
database = databases.Database(SQLALCHEMY_DATABASE_URL)

# создаем движок асинхронный SqlAlchemy
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# sync engine and Session
sync_engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autoflush=False, bind=engine)

# SQLAlchemy models below
Base = declarative_base()


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
