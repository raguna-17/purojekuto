# tests/conftest.py
import pytest
import asyncio
import os
from httpx import AsyncClient

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.main import app
from app.models import Base, User
from app.db import get_db
from app.auth import hash_password


@pytest.fixture(scope="session")
def event_loop():
    # pytest-asyncio 用に session スコープのループを提供
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def db_engine():
    DATABASE_URL = os.getenv("DATABASE_URL")
    engine = create_async_engine(DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture(scope="function")
async def db_session(db_engine):
    TestingSessionLocal = async_sessionmaker(
        db_engine, expire_on_commit=False, class_=AsyncSession
    )
    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()


@pytest.fixture(scope="function")
async def client(db_session):
    async def override_get_db():
        async with db_session as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url="http://testserver") as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
async def test_user(db_session: AsyncSession):
    user = User(
        email="test@example.com",
        hashed_password=hash_password("password123"),
        is_active=True
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user