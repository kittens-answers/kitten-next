import abc
from types import TracebackType
from typing import Sequence

from answers.domain import models
from answers.domain.commands import CreateAnswer, CreateQuestion
from answers.domain.specification import Specification


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


class AbstractUserRepository(abc.ABC):  # pragma: no cover
    @abc.abstractmethod
    async def get(self, user_id: str) -> models.User | None:
        ...

    @abc.abstractmethod
    async def create(self, user_id: str) -> models.User:
        ...

    @abc.abstractmethod
    async def get_or_create(self, user_id: str) -> models.User:
        ...


class AbstractAnswerRepository(abc.ABC):  # pragma: no cover
    @abc.abstractmethod
    async def get(self, dto: CreateAnswer) -> models.Answer | None:
        ...

    @abc.abstractmethod
    async def create(self, dto: CreateAnswer, user_id: str) -> models.Answer:
        ...

    @abc.abstractmethod
    async def get_or_create(self, dto: CreateAnswer, user_id: str) -> models.Answer:
        ...


class AbstractRepository(abc.ABC):  # pragma: no cover
    users: AbstractUserRepository
    questions: AbstractQuestionRepository
    answers: AbstractAnswerRepository

    async def __aenter__(self):
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ):
        await self.rollback()

    @abc.abstractmethod
    async def commit(self):
        ...

    @abc.abstractmethod
    async def rollback(self):
        ...
