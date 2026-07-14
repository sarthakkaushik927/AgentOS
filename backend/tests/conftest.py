import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.db.base import Base
from app.main import app
from app.db.session import get_db

# Use an in-memory SQLite for tests, but wait, the project uses Postgres.
# Since we use Postgres specific features (like UUID), SQLite might fail unless configured.
# Let's use an async SQLite for simple tests, or just mock the db.
# For now, let's use sqlite+aiosqlite:///:memory: and replace UUID if necessary, 
# or assume the test runner will provide a test postgres db. 
# We'll provide a generic sqlite URL for now to make the test run, but since UUID from asyncpg is used,
# we should probably just assume POSTGRES_TEST_URL is passed or fallback to sqlite with a warning.
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
