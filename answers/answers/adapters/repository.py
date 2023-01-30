import abc

from answers.domain.models import Question
from answers.service_layer.unit_of_work import AbstractUnitOfWork


class AbstractAnswerRepository(abc.ABC):
    @abc.abstractmethod  # pragma: no cover
    async def get_or_create_question(
        self, question: Question, uof: AbstractUnitOfWork
    ) -> str:
        raise NotImplementedError
