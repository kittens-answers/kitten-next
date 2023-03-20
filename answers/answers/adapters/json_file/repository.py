from pathlib import Path
from typing import Sequence

from pydantic import BaseModel

from answers.domain import commands, models
from answers.domain.abstract.exceptions import DoesExist
from answers.domain.abstract.repository import (
    AbstractAnswerRepository,
    AbstractAnswerTagRepository,
    AbstractQuestionRepository,
    AbstractRepository,
    AbstractUserRepository,
)
from answers.domain.specifications import Specification
from answers.domain.utils import new_id


class DB(BaseModel):
    users: list[models.User]
    questions: list[models.Question]
    answers: list[models.Answer]
    tags: list[models.AnswerTag]


class JSONFileUserRepository(AbstractUserRepository):
    def __init__(self, data: DB) -> None:
        self.data = data

    async def get(self, dto: commands.CreateUser) -> models.User | None:
        for user in self.data.users:
            if user.id == dto.user_id:
                return user

    async def create(self, dto: commands.CreateUser) -> models.User:
        user = models.User(id=dto.user_id)
        self.data.users.append(user)
        return user

    async def list(self, specs: list[Specification]) -> Sequence[models.User]:
        return self.data.users

    async def insert(self, model: models.User):
        self.data.users.append(models.User(id=model.id))


class JSONFileQuestionRepository(AbstractQuestionRepository):
    def __init__(self, data: DB) -> None:
        self.data = data

    async def get(self, dto: commands.CreateQuestion) -> models.Question | None:
        for question in self.data.questions:
            if all(
                [
                    question.text == dto.question_text,
                    question.question_type == dto.question_type,
                    question.options
                    == models.OptionDict(
                        options=frozenset(sorted(dto.options)),
                        extra_options=frozenset(sorted(dto.extra_options)),
                    ),
                ]
            ):
                return question

    async def create(self, dto: commands.CreateQuestion) -> models.Question:
        question = await self.get(dto=dto)
        if question is not None:
            raise DoesExist
        question = models.Question(
            text=dto.question_text,
            question_type=dto.question_type,
            created_by=dto.user_id,
            options=models.OptionDict(
                options=frozenset(sorted(dto.options)),
                extra_options=frozenset(sorted(dto.extra_options)),
            ),
            id=new_id(),
        )
        self.data.questions.append(question)
        return question

    async def insert(self, model: models.Question):
        self.data.questions.append(model)

    async def list(self, specs: list[Specification]) -> Sequence[models.Question]:
        return self.data.questions


class JSONFileAnswerRepository(AbstractAnswerRepository):
    def __init__(self, data: DB) -> None:
        self.data = data

    async def get(self, dto: commands.CreateAnswer) -> models.Answer | None:
        for answer in self.data.answers:
            if all(
                [
                    answer.question_id == dto.question_id,
                    answer.answer == models.AnswerDict(sorted(dto.answer)),
                ]
            ):
                return answer

    async def create(self, dto: commands.CreateAnswer) -> models.Answer:
        answer = models.Answer(
            id=new_id(),
            question_id=dto.question_id,
            answer=models.AnswerDict(sorted(dto.answer)),
            created_by=dto.user_id,
        )
        self.data.answers.append(answer)
        return answer

    async def list(self, specs: list[Specification]) -> Sequence[models.Answer]:
        return self.data.answers

    async def insert(self, model: models.Answer):
        self.data.answers.append(model)


class JSONFileAnswerTagRepository(AbstractAnswerTagRepository):
    def __init__(self, data: DB) -> None:
        self.data = data

    async def get(self, dto: commands.CreateTag) -> models.AnswerTag | None:
        for tag in self.data.tags:
            if all(
                [
                    tag.answer_id == dto.answer_id,
                    tag.created_by == dto.user_id,
                    tag.tag_name == dto.tag_name,
                ]
            ):
                return tag

    async def create(self, dto: commands.CreateTag) -> models.AnswerTag:
        tag = models.AnswerTag(
            id=new_id(),
            answer_id=dto.answer_id,
            created_by=dto.user_id,
            tag_name=dto.tag_name,
            value=dto.value,
        )
        self.data.tags.append(tag)
        return tag

    async def list(self, specs: list[Specification]) -> Sequence[models.AnswerTag]:
        return self.data.tags

    async def insert(self, model: models.AnswerTag):
        self.data.tags.append(model)


class JSONFileRepository(AbstractRepository):
    data: DB

    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path
        self.read_from_file()
        self.users = JSONFileUserRepository(data=self.data)
        self.questions = JSONFileQuestionRepository(data=self.data)
        self.answers = JSONFileAnswerRepository(data=self.data)
        self.tags = JSONFileAnswerTagRepository(data=self.data)

    def read_from_file(self):
        if self.file_path.exists():
            self.data = DB.parse_file(self.file_path)
        else:
            self.data = DB(users=[], questions=[], answers=[], tags=[])

    def save_to_file(self):
        with self.file_path.open(mode="w") as file:
            file.write(self.data.json(ensure_ascii=False, indent=4))

    async def commit(self):
        self.save_to_file()

    async def rollback(self):
        self.read_from_file()
