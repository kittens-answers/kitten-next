from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from answers.adapters.db.db_models import Option, Question, User


async def get_question(
    text: str, question_type: str, session: AsyncSession
) -> Question | None:
    res = await session.execute(
        select(Question)
        .options(
            joinedload(Question.options),
            joinedload(Question.extra_options),
            joinedload(Question.answers),
            joinedload(Question.user),
        )
        .where(
            Question.text == text,
            Question.question_type == question_type,
            Question.options.any(Option.text == "444"),
        )
        .limit(1)
    )
    try:
        return res.unique().scalars().one()
    except NoResultFound:
        return


async def get_or_create(
    text: str, question_type: str, user: User, session: AsyncSession
):
    question = await get_question(
        text=text, question_type=question_type, session=session
    )
    if question:
        return question
    question = Question(text=text, question_type=question_type)
    question.user = user
    session.add(question)
    return question
