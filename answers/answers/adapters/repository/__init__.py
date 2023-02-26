import abc

from answers.domain import models
from answers.domain.commands import CreateQuestion, CreateAnswer
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
