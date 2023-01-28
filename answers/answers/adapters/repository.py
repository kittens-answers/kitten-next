import abc
from uuid import uuid4

from answers.domain.models import Question, Options
from answers.service_layer.unit_of_work import AbstractUnitOfWork


class AbstractQuestionRepository(abc.ABC):
    @abc.abstractmethod
    async def add(self, question: Question, uof: AbstractUnitOfWork) -> str:
        raise NotImplementedError


class AbstractOptionsRepository(abc.ABC):
    @abc.abstractmethod
    async def add(self, options: Options, uow: AbstractUnitOfWork) -> str:
        raise NotADirectoryError


class FakeQuestionRepository(AbstractQuestionRepository):
    def __init__(self) -> None:
        self._data: dict[str, Question] = {}

    async def add(self, question: Question, uof: AbstractUnitOfWork) -> str:
        for data_id, data in self._data.items():
            if question == data:
                return data_id
        else:
            new_id = str(uuid4())
            self._data[new_id] = question
            return new_id


class FakeOptionsRepository(AbstractOptionsRepository):
    def __init__(self) -> None:
        self._data: dict[str, Options] = {}

    async def add(self, options: Options, uow: AbstractUnitOfWork) -> str:
        for data_id, data in self._data.items():
            if data == options:
                return data_id
        else:
            new_id = str(uuid4())
            self._data[new_id] = options
            return new_id
