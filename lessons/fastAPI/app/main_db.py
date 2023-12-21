import uvicorn
from database import SessionLocal, engine
from fastapi import Body, Depends, FastAPI, status
from fastapi.responses import JSONResponse
from models.models import Base, Todo

# создаем таблицы
Base.metadata.create_all(bind=engine)

my_app = FastAPI()


# определяем зависимость
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@my_app.post("/todos")
async def create_todo(data=Body(), db: SessionLocal = Depends(get_db)) -> JSONResponse:
    todo = Todo(**data)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    response_content = {
        "id": todo.id,
        "title": todo.title,
        "description": todo.description,
        "completed": todo.completed,
    }
    return JSONResponse(content=response_content, status_code=status.HTTP_201_CREATED)


@my_app.get("/todos/{todo_id}")
async def retrieve_todo(todo_id: int, db: SessionLocal = Depends(get_db)) -> JSONResponse:
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        return JSONResponse(content={"message": "Todo was not found."}, status_code=status.HTTP_404_NOT_FOUND)
    return todo


if __name__ == "__main__":
    # console command: uvicorn main:my_app --reload --port 8001
    uvicorn.run(
        "main_db:my_app",
        host="127.0.0.1",
        port=8001,
        reload=True,
    )
