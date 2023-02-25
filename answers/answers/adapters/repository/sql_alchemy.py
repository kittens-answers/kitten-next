from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from answers.adapters.db import db_models
from answers.adapters.repository import AbstractQuestionRepository
from answers.domain import models
from answers.domain.commands import CreateQuestion
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
                stmt = stmt.where(db_models.Question.text.icontains(spec.q))
        questions = (await self.session.scalars(stmt)).all()
        return tuple(map(self._from_db_model, questions))
