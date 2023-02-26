from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from answers.adapters.db import db_models
from answers.adapters.repository import (
    AbstractAnswerRepository,
    AbstractQuestionRepository,
    AbstractUserRepository,
)
from answers.domain import models
from answers.domain.commands import CreateAnswer, CreateQuestion
from answers.domain.specification import Specification, TextContains


class SQLAlchemyQuestionRepository(AbstractQuestionRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @staticmethod
    def _from_db_model(question: db_models.Question) -> models.Question:
        return models.Question(
            text=question.text,
            question_type=question.question_type,
            created_by=question.created_by,
            id=question.id,
            options=frozenset(question.options["options"]),
            extra_options=frozenset(question.options["extra_options"]),
        )

    async def get(self, dto: CreateQuestion) -> models.Question | None:
        stmt = (
            select(db_models.Question)
            .where(
                db_models.Question.text == dto.question_text,
                db_models.Question.question_type == dto.question_type,
                db_models.Question.options
                == db_models.OptionDict(
                    options=sorted(dto.options), extra_options=sorted(dto.extra_options)
                ),
            )
            .limit(1)
        )
        question = (await self.session.scalars(stmt)).first()
        if question is None:
            return
        else:
            return self._from_db_model(question)

    async def create(self, dto: CreateQuestion, user_id: str) -> models.Question:
        question = db_models.Question(
            text=dto.question_text,
            question_type=dto.question_type,
            options=db_models.OptionDict(
                options=sorted(dto.options), extra_options=sorted(dto.extra_options)
            ),
        )
        question.created_by = user_id
        self.session.add(question)
        await self.session.commit()
        return self._from_db_model(question)

    async def get_or_create(self, dto: CreateQuestion, user_id: str) -> models.Question:
        question = await self.get(dto=dto)
        if question is None:
            question = await self.create(dto=dto, user_id=user_id)
        return question

    async def list(self, specs: list[Specification]) -> Sequence[models.Question]:
        stmt = select(db_models.Question)
        for spec in specs:
            if isinstance(spec, TextContains):
                stmt = stmt.where(
                    db_models.Question.text.icontains(spec.q)  # type: ignore
                )
        questions = (await self.session.scalars(stmt)).all()
        return tuple(map(self._from_db_model, questions))


class SQLAlchemyUserRepository(AbstractUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @staticmethod
    def _from_db_model(user: db_models.User) -> models.User:
        return models.User(user_id=user.id)

    async def get(self, user_id: str) -> models.User | None:
        user = await self.session.get(db_models.User, user_id)
        if user is None:
            return
        else:
            return self._from_db_model(user)

    async def create(self, user_id: str) -> models.User:
        user = db_models.User(id=user_id)
        self.session.add(user)
        await self.session.commit()
        return self._from_db_model(user)

    async def get_or_create(self, user_id: str) -> models.User:
        user = await self.get(user_id=user_id)
        if user is None:
            user = await self.create(user_id=user_id)
        return user


class SQLAlchemyAnswerRepository(AbstractAnswerRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @staticmethod
    def _from_db_model(answer: db_models.Answer) -> models.Answer:
        return models.Answer(
            answer_id=answer.id,
            question_id=answer.question_id,
            answer=tuple(answer.answer.items()),
            created_by=answer.created_by,
        )

    async def get(self, dto: CreateAnswer) -> models.Answer | None:
        stmt = (
            select(db_models.Answer)
            .where(
                db_models.Answer.question_id == dto.question_id,
                db_models.Answer.answer == db_models.AnswerDict(sorted(dto.answer)),
            )
            .limit(1)
        )
        answer = (await self.session.scalars(stmt)).first()
        if answer is None:
            return None
        else:
            return self._from_db_model(answer)

    async def create(self, dto: CreateAnswer, user_id: str) -> models.Answer:
        answer = db_models.Answer(
            question_id=dto.question_id,
            answer=db_models.AnswerDict(sorted(dto.answer)),
        )
        answer.created_by = user_id
        self.session.add(answer)
        await self.session.commit()
        return self._from_db_model(answer)

    async def get_or_create(self, dto: CreateAnswer, user_id: str) -> models.Answer:
        answer = await self.get(dto=dto)
        if answer is None:
            answer = await self.create(dto=dto, user_id=user_id)
        return answer
