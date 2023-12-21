import uvicorn
from database import async_session, engine
from fastapi import Body, Depends, FastAPI, HTTPException, status
from models.models import Base, TodoCreate, TodoModel, TodoRetrieve
from sqlalchemy.ext.asyncio import AsyncSession


# создаем таблицы
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


my_app = FastAPI()

my_app.add_event_handler("startup", init_models)


async def get_db() -> AsyncSession:
    """
    Dependency function that yields db sessions
    """
    async with async_session() as session:
        yield session
        await session.commit()


@my_app.post("/todos", status_code=status.HTTP_201_CREATED, response_model=TodoRetrieve)
async def create_todo(data: TodoCreate = Body(), db: AsyncSession = Depends(get_db)) -> TodoRetrieve:
    todo = TodoModel(**data.model_dump())
    db.add(todo)
    try:
        await db.commit()
        await db.refresh(todo)
        return todo
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}: Failed to create user")


if __name__ == "__main__":
    # console command: uvicorn main:my_app --reload --port 8001
    uvicorn.run(
        "main_db_async_alch:my_app",
        host="127.0.0.1",
        port=8001,
        reload=True,
    )
