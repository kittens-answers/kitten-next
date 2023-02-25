import abc

from answers.domain import models
from answers.domain.commands import CreateQuestion
from answers.domain.specification import Specification
from typing import Sequence


class AbstractQuestionRepository(abc.ABC):  # pragma: no cover
    @abc.abstractmethod
    async def get(self, dto: CreateQuestion) -> models.Question | None:
        ...

    @abc.abstractmethod
    async def create(self, dto: CreateQuestion, user_id: str) -> models.Question:
        ...

    @abc.abstractmethod
    async def get_or_create(self, dto: CreateQuestion, user_id: str) -> models.Question:
        ...

    @abc.abstractmethod
    async def list(self, specs: list[Specification]) -> Sequence[models.Question]:
        ...
