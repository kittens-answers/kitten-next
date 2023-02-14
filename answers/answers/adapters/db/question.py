from sqlalchemy import func, intersect, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from answers.adapters.db.db_models import (
    ExtraOptionItem,
    OptionItem,
    Question,
)


from answers.domain.commands import CreateQuestion


async def get(dto: CreateQuestion, session: AsyncSession) -> Question | None:
    stmt1 = (
        select(Question)
        .where(
            Question.text == dto.question_text,
            Question.question_type == dto.question_type,
        )
        .join(OptionItem, full=True)
        .options(selectinload(Question.options), selectinload(Question.extra_options))
        .group_by(Question.options)
        .having(func.count(OptionItem.text) == len(dto.options))
    )
    if dto.options:
        stmt1 = stmt1.where(
            *(Question.options.any(OptionItem.text == item) for item in dto.options)
        )
    stmt2 = (
        select(Question)
        .where(
            Question.text == dto.question_text,
            Question.question_type == dto.question_type,
        )
        .join(ExtraOptionItem)
        .options(selectinload(Question.options), selectinload(Question.extra_options))
        .group_by(Question.extra_options)
        .having(func.count(ExtraOptionItem.text) == len(dto.extra_options))
    )
    if dto.extra_options:
        stmt2 = stmt2.where(
            *(
                Question.extra_options.any(ExtraOptionItem.text == item)
                for item in dto.extra_options
            )
        )

    return (
        (
            await session.execute(
                select(Question)
                .limit(1)
                .from_statement(intersect(stmt1, stmt2))
                .options(
                    selectinload(Question.options), selectinload(Question.extra_options)
                )
            )
        )
        .scalars()
        .first()
    )


async def create(dto: CreateQuestion, user_id: str, session: AsyncSession) -> Question:
    question = Question(text=dto.question_text, question_type=dto.question_type)
    question.created_by = user_id
    for option in dto.options:
        question.options.append(OptionItem(text=option))
    for extra_option in dto.extra_options:
        question.extra_options.append(ExtraOptionItem(text=extra_option))
    session.add(question)
    await session.commit()
    return question


async def get_or_create(
    dto: CreateQuestion, user_id: str, session: AsyncSession
) -> Question:
    question = await get(dto=dto, session=session)
    if question is None:
        question = await create(dto=dto, user_id=user_id, session=session)
    return question
