from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from answers.domain.aggregate import QuestionWithAnswer
from answers.domain.bootstrap import BootStrap
from answers.domain.specifications import TextContains

boot = BootStrap()


@asynccontextmanager
async def lifespan(app):
    async with boot:
        yield


app = FastAPI(lifespan=lifespan)


async def get_agr():
    return await boot.get_qwa_aggregate()


@app.post("/search")
async def search(q: str, agr: QuestionWithAnswer = Depends(get_agr)):
    async with agr.repository:
        return await agr.repository.questions.list([TextContains(q=q)])
