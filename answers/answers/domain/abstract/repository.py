import abc
from operator import getitem
from typing import Self

from answers.domain import commands, models
from answers.domain.exceptions import repository_exc


class AbstractRepository(abc.ABC):  # pragma: no cover
    @abc.abstractmethod
    async def create_user(self, command: commands.CreateUser) -> models.User:
        ...

    @abc.abstractmethod
    async def get_user_by_id(self, user_id: str) -> models.User:
        ...

    @abc.abstractmethod
    async def create_question(self, user: models.User, command: commands.CreateQuestion) -> models.Question:
        ...

    @abc.abstractmethod
    async def get_question_by_id(self, question_id: str) -> models.Question:
        ...

    @abc.abstractmethod
    async def create_answer(self, user: models.User, question_id: str, command: commands.CreateAnswer) -> models.Answer:
        ...

    @abc.abstractmethod
    async def get_answer_by_id(self, answer_id: str) -> models.Answer:
        ...

    @abc.abstractmethod
    async def add_tag(self, user: models.User, answer_id: str, command: commands.CreateTag) -> models.Tag:
        ...

    @abc.abstractmethod
    async def __aenter__(self) -> Self:
        ...

    @abc.abstractmethod
    async def __aexit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> bool | None:
        ...


def validate_answer(
    options: frozenset[str],
    extra_options: frozenset[str],
    question_type: models.QuestionType,
    answer: list[tuple[str, str]],
) -> bool:
    left = [getitem(v, 0) for v in answer]
    right = [getitem(v, 1) for v in answer]
    if options and options != frozenset(left):
        raise repository_exc.AnswerCanNotBeAddedToQuestion

    match question_type:
        case models.QuestionType.ONE:
            if right.count(str(True)) != 1 or (right.count(str(False)) + 1) != len(right):
                raise repository_exc.AnswerCanNotBeAddedToQuestion
        case models.QuestionType.MANY:
            true_count = right.count(str(True))
            if true_count < 1 or (right.count(str(False)) + true_count) != len(right):
                raise repository_exc.AnswerCanNotBeAddedToQuestion
        case models.QuestionType.ORDER:
            if sorted(right) != [str(v) for v in range(1, len(right) + 1)]:
                raise repository_exc.AnswerCanNotBeAddedToQuestion
        case models.QuestionType.MATCH:
            if extra_options and extra_options != frozenset(right):
                raise repository_exc.AnswerCanNotBeAddedToQuestion

    return True
