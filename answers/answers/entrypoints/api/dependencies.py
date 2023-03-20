from typing import Annotated

from fastapi import Depends, FastAPI, Request

from answers.domain.aggregate import QuestionWithAnswer


async def get_agr(request: Request):
    app: FastAPI = request.app
    boot = app.state.boot
    return await boot.get_qwa_aggregate()


Agr = Annotated[QuestionWithAnswer, Depends(get_agr)]
