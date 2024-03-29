from datetime import datetime

import uvicorn
from fastapi import Body, Depends, FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import (
    CustomExceptionA,
    UserNotFoundException,
    http_exception_handler,
    user_not_found_handler,
)
from app.models.db_models import Base, TodoNewModel, User, async_session, engine
from app.models.exceptions_models import CustomExceptionModel
from app.models.models_user_validate import TodoCreate, TodoRetrieve, TodoUpdate
from app.models.models_user_validate import User as UserValidateModel
from app.models.models_user_validate import UserRetrieve


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


# register handler
my_app.add_exception_handler(UserNotFoundException, user_not_found_handler)
my_app.add_exception_handler(RequestValidationError, http_exception_handler)


@my_app.post("/user/", status_code=status.HTTP_201_CREATED, response_model=UserRetrieve)
async def create_user(data: UserValidateModel = Body(), db: AsyncSession = Depends(get_db)) -> UserRetrieve:
    data.username = data.username or "Undefined Monte-Cristo"
    user = User(**data.model_dump())
    db.add(user)
    try:
        await db.commit()
        await db.refresh(user)
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}: Failed to create user")


@my_app.get("/user/{user_id}", status_code=status.HTTP_200_OK, response_model=UserRetrieve)
async def retrieve_user(user_id: int, db: AsyncSession = Depends(get_db)) -> UserRetrieve:
    start_time = datetime.now()
    query = select(User).filter(User.id == user_id)
    try:
        user_iter = await db.execute(query)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}: Failed to fetch user from database"
        )
    user = user_iter.scalars().first()
    if user is None:
        raise UserNotFoundException(
            detail="user_id",
            message="User with user_id was not found.",
            status_code=status.HTTP_404_NOT_FOUND,
            headers={"X-ErrorHandleTime": str(datetime.now() - start_time)},
        )
    return user


if __name__ == "__main__":
    # from fastAPI do: PYTHONPATH=. python app/main_db_alembic.py -m
    # make startserver PATH_TO_MAIN='app/main_db_alembic.py'
    # console command: uvicorn main:my_app --reload --port 8001
    uvicorn.run(
        "main_db_alembic:my_app",
        host="127.0.0.1",
        port=8001,
        reload=True,
    )
