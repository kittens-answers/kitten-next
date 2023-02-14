from sqlalchemy import func, select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from answers.adapters.db.db_models import Answer, AnswerItem


from answers.domain.commands import CreateAnswer


async def get(dto: CreateAnswer, session: AsyncSession) -> Answer | None:
    stmt = (
        select(Answer)
        .limit(1)
        .where(Answer.question_id == dto.question_id)
        .join(AnswerItem, full=True)
        .options(selectinload(Answer.answer))
        .group_by(Answer.answer)
        .having(func.count(AnswerItem.left) == len(dto.answer))
        .where(
            *(
                Answer.answer.any(
                    and_(AnswerItem.left == left, AnswerItem.right == right)
                )
                for (left, right) in dto.answer
            )
        )
    )
    return (await session.execute(stmt)).scalars().first()


async def create(dto: CreateAnswer, user_id: str, session: AsyncSession) -> Answer:
    answer = Answer(question_id=dto.question_id)
    answer.created_by = user_id
    for (left, right) in dto.answer:
        answer.answer.append(AnswerItem(left=left, right=right))
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
