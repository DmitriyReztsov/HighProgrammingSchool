import uvicorn
from exceptions import CustomExceptionA
from fastapi import Body, Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from models.db_models import Base, TodoNewModel, async_session, engine
from models.exceptions_models import CustomException as CustomExceptionModel
from models.models import TodoCreate, TodoRetrieve, TodoUpdate
from sqlalchemy import select
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
    todo = TodoNewModel(**data.model_dump())
    db.add(todo)
    try:
        await db.commit()
        await db.refresh(todo)
        return todo
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}: Failed to create user")


@my_app.get("/todos/", status_code=status.HTTP_200_OK)
async def list_todo(db: AsyncSession = Depends(get_db)) -> list[TodoRetrieve]:
    query = select(TodoNewModel)
    try:
        todo_iter = await db.execute(query)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}: Failed to fetch user from database"
        )
    todos = todo_iter.scalars().all()
    if todos is None:
        return JSONResponse(content={"message": "Todo was not found."}, status_code=status.HTTP_404_NOT_FOUND)
    return todos


@my_app.get("/todos/{todo_id}", status_code=status.HTTP_200_OK, response_model=TodoRetrieve)
async def retrieve_todo(todo_id: int, db: AsyncSession = Depends(get_db)) -> TodoRetrieve:
    query = select(TodoNewModel).filter(TodoNewModel.id == todo_id)
    try:
        todo_iter = await db.execute(query)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}: Failed to fetch user from database"
        )
    todo = todo_iter.scalars().first()
    if todo is None:
        return JSONResponse(content={"message": "Todo was not found."}, status_code=status.HTTP_404_NOT_FOUND)
    return todo


@my_app.put("/todos/{todo_id}", status_code=status.HTTP_200_OK, response_model=TodoRetrieve)
async def update_todo(todo_id: int, data: TodoUpdate = Body(), db: AsyncSession = Depends(get_db)) -> TodoRetrieve:
    try:
        todo_current = await db.get(TodoNewModel, todo_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}: Failed to fetch user from database"
        )
    if not todo_current:
        return JSONResponse(content={"message": "Todo was not found."}, status_code=status.HTTP_404_NOT_FOUND)

    for attr_name, attr_value in data.model_dump().items():
        if attr_value is None:
            continue
        setattr(todo_current, attr_name, attr_value)
    try:
        await db.commit()
        await db.refresh(todo_current)
        return todo_current
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}: Failed to create user")


@my_app.delete("/todos/{todo_id}", status_code=status.HTTP_200_OK, response_model=TodoRetrieve)
async def delete_todo(todo_id: int, db: AsyncSession = Depends(get_db)) -> TodoRetrieve:
    try:
        todo_current = await db.get(TodoNewModel, todo_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}: Failed to fetch user from database"
        )
    if not todo_current:
        return JSONResponse(content={"message": "Todo was not found."}, status_code=status.HTTP_404_NOT_FOUND)

    try:
        await db.delete(todo_current)
        await db.commit()
        return todo_current
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}: Failed to create user")


@my_app.exception_handler(CustomExceptionA)
async def custom_exception_handler(request: Request, exc: CustomExceptionModel):
    return JSONResponse(content={exc.message: exc.detail}, status_code=exc.status_code)


@my_app.get("/items/{item_id}/")
async def read_item(item_id: int):
    if item_id == 42:
        raise CustomExceptionA(detail="Item not found", status_code=444, message="Message")
    return {"item_id": item_id}


if __name__ == "__main__":
    # console command: uvicorn main:my_app --reload --port 8001
    uvicorn.run(
        "main_db_alembic:my_app",
        host="127.0.0.1",
        port=8001,
        reload=True,
    )
