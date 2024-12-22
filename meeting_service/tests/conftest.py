import os

import pytest
from app.db import get_db
from app.main import app
from app.models import Base
from app.routers.meeting_router import get_attendee
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

TEST_DATABASE_PATH = "./test.db"
TEST_DATABASE_URL = f"sqlite+aiosqlite:///{TEST_DATABASE_PATH}"


@pytest.fixture(scope="session")
async def engine():
    if os.path.exists(TEST_DATABASE_PATH):
        os.remove(TEST_DATABASE_PATH)
    _engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    yield _engine
    await _engine.dispose()


@pytest.fixture(scope="function")
async def tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def test_client(engine, tables):
    async_session_factory = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async def override_get_db():
        async with async_session_factory() as session:
            yield session

    # Override the get_db dependency
    app.dependency_overrides[get_db] = override_get_db

    # Mock the attendee dependency globally
    app.dependency_overrides[get_attendee] = lambda: {"private_notes": "Mock notes"}

    # Providing both session and client
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as client:
        # Provide both the client and a fresh session for direct use in tests
        async with async_session_factory() as session:
            yield client, session
