from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from answers.adapters.db import BootStrap
from answers.adapters.repository.sql_alchemy import SQLAlchemyRepository
from answers.domain.aggregate import QuestionWithAnswer
from answers.domain.specifications import TextContains

boot = BootStrap()


@asynccontextmanager
async def lifespan(app):
    await boot.start()
    yield
    await boot.stop()


app = FastAPI(lifespan=lifespan)


async def get_agr():
    repo = SQLAlchemyRepository(session_factory=boot.async_session)
    return QuestionWithAnswer(repo)


@app.post("/search")
async def search(q: str, agr: QuestionWithAnswer = Depends(get_agr)):
    async with agr.repository:
        return await agr.repository.questions.list([TextContains(q=q)])
