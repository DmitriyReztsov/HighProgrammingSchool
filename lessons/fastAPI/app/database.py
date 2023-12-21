import databases
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
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
