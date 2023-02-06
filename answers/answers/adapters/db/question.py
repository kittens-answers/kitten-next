from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from answers.adapters.db.db_models import (
    OptionItem,
    Question,
    User,
    ExtraOptionItem,
    Option,
)


async def get_question(
    text: str,
    question_type: str,
    option: tuple[str],
    extra_option: tuple[str],
    session: AsyncSession,
) -> Question | None:
    res = await session.execute(
        select(Question)
        .options(
            joinedload(Question.option),
            joinedload(Question.answers),
            joinedload(Question.user),
        )
        .where(
            Question.text == text,
            Question.question_type == question_type,
            *(Option.options.any(OptionItem.text == op) for op in option),
            *(
                Option.extra_options.any(ExtraOptionItem.text == eop)
                for eop in extra_option
            )
        )
        .limit(1)
    )
    try:
        return res.unique().scalars().one()
    except NoResultFound:
        return


async def get_or_create(
    text: str,
    question_type: str,
    user: User,
    option: tuple[str],
    extra_option: tuple[str],
    session: AsyncSession,
):
    question = await get_question(
        text=text,
        question_type=question_type,
        option=option,
        extra_option=extra_option,
        session=session,
    )
    if question:
        return question
    question = Question(text=text, question_type=question_type)
    question.user = user
    session.add(question)
    return question
