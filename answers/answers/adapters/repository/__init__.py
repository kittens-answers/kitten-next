import abc

from answers.domain import models
from answers.domain.commands import CreateQuestion


class AbstractQuestionRepository(abc.ABC):
    @abc.abstractmethod  # pragma: no cover
    async def get(self, dto: CreateQuestion) -> models.Question | None:
        ...

    @abc.abstractmethod  # pragma: no cover
    async def create(self, dto: CreateQuestion, user_id: str) -> models.Question:
        ...
