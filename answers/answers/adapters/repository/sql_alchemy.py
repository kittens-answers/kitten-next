from sqlalchemy.ext.asyncio import AsyncSession

from answers.adapters.db.db_models import Question
from answers.adapters.db.question import get as get_question, create as create_question
from answers.adapters.repository import AbstractQuestionRepository
from answers.domain import models
from answers.domain.commands import CreateQuestion


class SQLAlchemyQuestionRepository(AbstractQuestionRepository):
    async def get(
        self, dto: CreateQuestion, uow: AsyncSession
    ) -> models.Question | None:
        def _filter(q: Question):
            return (
                frozenset(v.text for v in q.option.options) == dto.options
                and frozenset(v.text for v in q.option.extra_options)
                == dto.extra_options
            )

        questions = await get_question(dto=dto, session=uow)
        filter(_filter, questions)
        if questions:
            question = questions[0]
            return models.Question(
                text=question.text,
                question_type=models.QuestionType(question.question_type),
                created_by=question.created_by,
                id=question.id,
                options=frozenset(v.text for v in question.option.options),
                extra_options=frozenset(v.text for v in question.option.extra_options),
            )

    async def create(
        self, dto: CreateQuestion, user_id: str, uow: AsyncSession
    ) -> None:
        await create_question(dto=dto, user_id=user_id, session=uow)
