import abc

from answers.domain import models
from answers.domain.commands import CreateQuestion
from answers.service_layer.unit_of_work import AbstractUOW


class AbstractQuestionRepository(abc.ABC):
    @abc.abstractmethod  # pragma: no cover
    async def get(
        self, dto: CreateQuestion, uow: AbstractUOW
    ) -> models.Question | None:
        ...

    @abc.abstractmethod  # pragma: no cover
    async def create(
        self, dto: CreateQuestion, user_id: str, uow: AbstractUOW
    ) -> models.Question:
        ...
