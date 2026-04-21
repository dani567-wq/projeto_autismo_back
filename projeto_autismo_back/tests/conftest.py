from contextlib import contextmanager
from datetime import datetime

import factory
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool

from app.domains.users.models import User
from app.main import app
from app.shared.db.database import get_session
from app.shared.db.registry import mapper_registry
from app.shared.security import get_password_hash


# ── Engine de testes (SQLite in-memory) ──────────────────────────────── #


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(
        'sqlite+aiosqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.drop_all)


# ── Client HTTP com override de sessão ───────────────────────────────── #


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


# ── Helper para mockar timestamps do banco ───────────────────────────── #


@contextmanager
def _mock_db_time(*, model, time=datetime(2024, 1, 1)):
    def fake_time_handler(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_handler)
    yield time
    event.remove(model, 'before_insert', fake_time_handler)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


# ── Factories ────────────────────────────────────────────────────────── #


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')


# ── Fixtures de entidades ─────────────────────────────────────────────── #


@pytest_asyncio.fixture
async def user(session):
    password = 'testtest'
    db_user = UserFactory(password=get_password_hash(password))
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    db_user.clean_password = password
    return db_user


@pytest_asyncio.fixture
async def other_user(session):
    password = 'testtest'
    db_user = UserFactory(password=get_password_hash(password))
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    db_user.clean_password = password
    return db_user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    return response.json()['access_token']
