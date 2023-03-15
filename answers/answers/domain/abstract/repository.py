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
    async def insert(self, model: models.Question):
        ...

    async def get_or_create(
        self, dto: commands.CreateQuestion
    ) -> tuple[models.Question, bool]:
        question = await self.get(dto=dto)
        if question:
            return (question, False)
        else:
            question = await self.create(dto=dto)
            return (question, True)

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
    async def list(self, specs: list[Specification]) -> Sequence[models.User]:
        ...

    @abc.abstractmethod
    async def insert(self, model: models.User):
        ...

    async def get_or_create(self, dto: commands.CreateUser) -> tuple[models.User, bool]:
        user = await self.get(dto=dto)
        if user:
            return (user, False)
        else:
            user = await self.create(dto=dto)
            return (user, True)


class AbstractAnswerRepository(abc.ABC):  # pragma: no cover
    @abc.abstractmethod
    async def get(self, dto: commands.CreateAnswer) -> models.Answer | None:
        ...

    @abc.abstractmethod
    async def create(self, dto: commands.CreateAnswer) -> models.Answer:
        ...

    @abc.abstractmethod
    async def list(self, specs: list[Specification]) -> Sequence[models.Answer]:
        ...

    @abc.abstractmethod
    async def insert(self, model: models.Answer):
        ...

    async def get_or_create(
        self, dto: commands.CreateAnswer
    ) -> tuple[models.Answer, bool]:
        answer = await self.get(dto=dto)
        if answer:
            return (answer, False)
        else:
            answer = await self.create(dto=dto)
            return (answer, True)


class AbstractAnswerTagRepository(abc.ABC):  # pragma: no cover
    @abc.abstractmethod
    async def get(self, dto: commands.CreateTag) -> models.AnswerTag | None:
        ...

    @abc.abstractmethod
    async def create(self, dto: commands.CreateTag) -> models.AnswerTag:
        ...

    @abc.abstractmethod
    async def list(self, specs: list[Specification]) -> Sequence[models.AnswerTag]:
        ...

    @abc.abstractmethod
    async def insert(self, model: models.AnswerTag):
        ...

    async def get_or_create(
        self, dto: commands.CreateTag
    ) -> tuple[models.AnswerTag, bool]:
        tag = await self.get(dto=dto)
        if tag:
            return (tag, False)
        else:
            tag = await self.create(dto=dto)
            return (tag, True)


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
