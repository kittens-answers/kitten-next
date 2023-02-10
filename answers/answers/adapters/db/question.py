from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from answers.adapters.db.db_models import ExtraOptionItem, Option, OptionItem, Question
from answers.domain.commands import CreateQuestion


async def get(dto: CreateQuestion, session: AsyncSession) -> Sequence[Question]:
    res = await session.execute(
        select(Question, Option)
        .join(Option)
        .options(
            joinedload(Question.option),
            joinedload(Question.user),
            joinedload(Option.options),
            joinedload(Option.extra_options),
        )
        .where(
            Question.text == dto.question_text,
            Question.question_type == dto.question_type,
        )
    )
    return res.unique().scalars().all()


async def create(
    dto: CreateQuestion,
    user_id: str,
    session: AsyncSession,
):
    question = Question(text=dto.question_text, question_type=dto.question_type)
    question.created_by = user_id
    option = Option()
    for _option in dto.options:
        option.options.append(OptionItem(text=_option))
    for extra_option in dto.extra_options:
        option.extra_options.append(ExtraOptionItem(text=extra_option))
    question.option = option
    session.add(question)
