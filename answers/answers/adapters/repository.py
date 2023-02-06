import abc

from answers.domain.commands import CreateQuestion
from answers.service_layer.unit_of_work import AbstractUnitOfWork


class AbstractAnswerRepository(abc.ABC):
    @abc.abstractmethod  # pragma: no cover
    async def get_or_create_question(
        self, question: CreateQuestion, uof: AbstractUnitOfWork
    ) -> str:
        raise NotImplementedError


class SQLAlchemyRepository(AbstractAnswerRepository):
    async def get_or_create_question(
        self, question: CreateQuestion, uof: AbstractUnitOfWork
    ) -> str:
        ...
