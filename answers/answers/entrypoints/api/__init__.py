from contextlib import asynccontextmanager

from fastapi import FastAPI

from answers.adapters.sqlalchemy.repository import SQLAlchemyRepository
from answers.entrypoints.api.app_builder import get_app


@asynccontextmanager
async def lifespan(app: FastAPI):  # pragma: no cover
    async with SQLAlchemyRepository() as repo:
        app.state.repo = repo
        yield


app = get_app(lifespan=lifespan)
