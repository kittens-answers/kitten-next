from fastapi import APIRouter

from answers.domain.specifications import TextContains
from answers.entrypoints.api.dependencies import Agr

router = APIRouter()


@router.post("/search")
async def search(q: str, agr: Agr):
    async with agr.repository:
        return await agr.repository.questions.list([TextContains(q=q)])
