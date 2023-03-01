import abc
from types import TracebackType
from typing import Sequence

from answers.domain import commands, models
from answers.domain.specifications import Specification


class AbstractQuestionRepository(abc.ABC):  # pragma: no cover
    @abc.abstractmethod
    async def get(self, dto: commands.CreateQuestion) -> models.Question | None:
        ...

    @abc.abstractmethod
    async def create(self, dto: commands.CreateQuestion) -> models.Question:
        ...

    @abc.abstractmethod
    async def get_or_create(self, dto: commands.CreateQuestion) -> models.Question:
        ...

    @abc.abstractmethod
    async def list(self, specs: list[Specification]) -> Sequence[models.Question]:
        ...


class AbstractUserRepository(abc.ABC):  # pragma: no cover
    @abc.abstractmethod
    async def get(self, dto: commands.CreateUser) -> models.User | None:
        ...

    @abc.abstractmethod
    async def create(self, dto: commands.CreateUser) -> models.User:
        ...

    @abc.abstractmethod
    async def get_or_create(self, dto: commands.CreateUser) -> models.User:
        ...


class AbstractAnswerRepository(abc.ABC):  # pragma: no cover
    @abc.abstractmethod
    async def get(self, dto: commands.CreateAnswer) -> models.Answer | None:
        ...

    @abc.abstractmethod
    async def create(self, dto: commands.CreateAnswer) -> models.Answer:
        ...

    @abc.abstractmethod
    async def get_or_create(self, dto: commands.CreateAnswer) -> models.Answer:
        ...


class AbstractAnswerTagRepository(abc.ABC):  # pragma: no cover
    @abc.abstractmethod
    async def get(self, dto: commands.CreateTag) -> models.AnswerTag | None:
        ...

    @abc.abstractmethod
    async def create(self, dto: commands.CreateTag) -> models.AnswerTag:
        ...

    @abc.abstractmethod
    async def create_or_update(self, dto: commands.CreateTag) -> models.AnswerTag:
        ...


class AbstractRepository(abc.ABC):  # pragma: no cover
    users: AbstractUserRepository
    questions: AbstractQuestionRepository
    answers: AbstractAnswerRepository
    tags: AbstractAnswerTagRepository

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
