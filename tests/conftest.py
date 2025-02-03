from unittest.mock import AsyncMock

from httpx import ASGITransport, AsyncClient
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.api.dependencies import get_group_service, get_role_service, get_user_service
from app.db.models import Base
from app.db.repositories.group_repo import GroupRepository
from app.db.repositories.role_repo import RoleRepository
from app.db.repositories.user_repo import UserRepository
from app.db.session import get_db
from app.main import app
from app.services.group_service import GroupService
from app.services.role_service import RoleService
from app.services.user_service import UserService

# Use an in-memory SQLite database for tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(name="test_engine", scope="session")
async def _test_engine():
    # Create an in-memory SQLite engine
    _engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    yield _engine
    await _engine.dispose()


@pytest.fixture(scope="session")
async def tables(test_engine):
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(name="test_db_session", scope="function")
async def _test_db_session():
    # Create an isolated in-memory SQLite database for each test
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async_session_factory = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_factory() as session:
        yield session

    # Dispose of the engine after the test
    await engine.dispose()


@pytest.fixture
async def test_client(test_db_session, mock_redis_client):
    app.dependency_overrides[get_db] = lambda: test_db_session

    app.dependency_overrides[get_group_service] = lambda: GroupService(
        GroupRepository(test_db_session), mock_redis_client
    )

    app.dependency_overrides[get_role_service] = lambda: RoleService(
        RoleRepository(test_db_session), mock_redis_client
    )

    app.dependency_overrides[get_user_service] = lambda: UserService(
        UserRepository(test_db_session), mock_redis_client
    )

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as client:
        yield client


@pytest.fixture(name="mock_redis_client")
async def _mock_redis_client():
    mock = AsyncMock()
    mock.publish = AsyncMock()
    return mock


@pytest.fixture
async def user_service(test_db_session, mock_redis_client):
    repo = UserRepository(test_db_session)
    service = UserService(repo, mock_redis_client)
    return service


@pytest.fixture
async def group_service(test_db_session, mock_redis_client):
    repo = GroupRepository(test_db_session)
    service = GroupService(repo, mock_redis_client)
    return service


@pytest.fixture
async def role_service(test_db_session, mock_redis_client):
    repo = RoleRepository(test_db_session)
    service = RoleService(repo, mock_redis_client)
    return service
