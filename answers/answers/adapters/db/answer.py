from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from answers.adapters.db.db_models import Answer, AnswerDict


from answers.domain.commands import CreateAnswer


async def get(dto: CreateAnswer, session: AsyncSession) -> Answer | None:
    stmt = (
        select(Answer)
        .where(
            Answer.question_id == dto.question_id,
            Answer.answer == AnswerDict(sorted(dto.answer)),
        )
        .limit(1)
    )
    return (await session.scalars(stmt)).first()


async def create(dto: CreateAnswer, user_id: str, session: AsyncSession) -> Answer:
    answer = Answer(
        question_id=dto.question_id,
        answer=AnswerDict(sorted(dto.answer)),
    )
    answer.created_by = user_id
    session.add(answer)
    await session.commit()
    return answer


async def get_or_create(
    dto: CreateAnswer, user_id: str, session: AsyncSession
) -> Answer:
    answer = await get(dto=dto, session=session)
    if answer is None:
        answer = await create(dto=dto, user_id=user_id, session=session)
    return answer
