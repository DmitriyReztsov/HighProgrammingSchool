import pytest
import pytest_asyncio
from httpx import AsyncClient

from app.main_db_alembic import my_app
from app.models.db_models import Base, create_async_engine

# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./app/test.db"


# @pytest.mark.asyncio
@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database():
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# @pytest.mark.asyncio
async def test_get_todos():
    async with AsyncClient(app=my_app, base_url="http://127.0.0.1") as ac:
        response = await ac.get("/todos/")
    print(">>> response get <<<", response.content)

    assert response.status_code == 200
    assert response.json() == []


# @pytest.mark.asyncio
async def test_create_todo():
    data = {"title": "Test title", "description": "Test description"}
    async with AsyncClient(app=my_app, base_url="http://127.0.0.1") as ac:
        response = await ac.post("/todos", json=data, headers={"Content-Type": "application/json"})
    print(">>> response post <<<", response.content)
    assert response.status_code == 201
    assert response.json()["title"] == "Test title"
