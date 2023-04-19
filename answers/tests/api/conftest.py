from contextlib import asynccontextmanager

import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient

from answers.adapters.sqlalchemy.repository import SQLAlchemyRepository
from answers.entrypoints.api.app_builder import get_app

pytestmark = pytest.mark.anyio


@pytest.fixture
async def app(repository: SQLAlchemyRepository):
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.repo = repository
        yield

    return get_app(lifespan=lifespan)


@pytest.fixture
async def client(app: FastAPI):
    async with LifespanManager(app) as manager, AsyncClient(app=manager.app, base_url="http://test") as client:
        yield client
