from typing import Annotated, cast

from fastapi import Depends, FastAPI, Request

from answers.domain import models
from answers.domain.abstract.repository import AbstractRepository


async def _get_repository(request: Request):
    app: FastAPI = request.app
    repo = cast(AbstractRepository, app.state.repo)
    return repo


Repository = Annotated[AbstractRepository, Depends(_get_repository)]


async def _get_current_user(user_id: str, repository: Repository) -> models.User:
    return await repository.get_user_by_id(user_id)


CurrentUser = Annotated[models.User, Depends(_get_current_user)]
