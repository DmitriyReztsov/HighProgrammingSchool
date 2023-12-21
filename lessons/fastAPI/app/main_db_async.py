from contextlib import asynccontextmanager

import uvicorn
from databases import Database
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from models.models import UserCreate, UserReturn


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


my_app = FastAPI(lifespan=lifespan)

# URL для PostgreSQL (измените его под свою БД)
DATABASE_URL = "sqlite+aiosqlite:///./HighProgrammingSchool/lessons/fastAPI/app/sql_app.db"

database = Database(DATABASE_URL)


# тут устанавливаем условия подключения к базе данных и отключения
# можно использовать в роутах контекстный менеджер async with Database(...) as db: etc
# @app.on_event("startup")
# async def startup_database():
#     await database.connect()

# @app.on_event("shutdown")
# async def shutdown_database():
#     await database.disconnect()


@my_app.post("/create_table")
async def create_table() -> JSONResponse:
    query = "CREATE TABLE users (id INTEGER PRIMARY KEY, username VARCHAR(255) NOT NULL, email VARCHAR(255) NOT NULL)"
    try:
        await database.execute(
            query=query,
        )
        return JSONResponse(content={"message": "Таблица успешно создана"}, status_code=status.HTTP_201_CREATED)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}: Failed to create user")


# создание роута для создания юзеров
@my_app.post("/users/", response_model=UserReturn)
async def create_user(user: UserCreate) -> JSONResponse:
    query = "INSERT INTO users (username, email) VALUES (:username, :email) RETURNING id"
    values = {"username": user.username, "email": user.email}
    try:
        user_id = await database.execute(query=query, values=values)
        return JSONResponse(content={**user.model_dump(), "id": user_id}, status_code=status.HTTP_201_CREATED)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}: Failed to create user")


# маршрут для получения информации о юзере по ID
@my_app.get("/user/{user_id}", response_model=UserReturn)
async def get_user(user_id: int) -> JSONResponse:
    query = "SELECT * FROM users WHERE id = :user_id"
    values = {"user_id": user_id}
    try:
        result = await database.fetch_one(query=query, values=values)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}: Failed to fetch user from database"
        )
    if result:
        return JSONResponse(
            content=UserReturn(username=result["username"], email=result["email"], id=result["id"]).model_dump(),
            status_code=status.HTTP_200_OK,
        )
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


# роут для обновления информации о юзере по ID
@my_app.put("/user/{user_id}", response_model=UserReturn)
async def update_user(user_id: int, user: UserCreate) -> JSONResponse:
    query = "UPDATE users SET username = :username, email = :email WHERE id = :user_id"
    values = {"user_id": user_id, "username": user.username, "email": user.email}
    try:
        await database.execute(query=query, values=values)
        return JSONResponse(content={**user.model_dump(), "id": user_id}, status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}: Failed to update user in database"
        )


# роут для удаления информации о юзере по ID
@my_app.delete("/user/{user_id}", response_model=dict)
async def delete_user(user_id: int) -> JSONResponse:
    query = "DELETE FROM users WHERE id = :user_id RETURNING id"
    values = {"user_id": user_id}
    try:
        deleted_rows = await database.fetch_all(query=query, values=values)
        print(">>> deleted <<<", deleted_rows)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}: Failed to delete user from database"
        )
    if deleted_rows:
        return JSONResponse(content={"message": "User deleted successfully"}, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


if __name__ == "__main__":
    # console command: uvicorn main:my_app --reload --port 8001
    uvicorn.run(
        "main_db_async:my_app",
        host="127.0.0.1",
        port=8001,
        reload=True,
    )
