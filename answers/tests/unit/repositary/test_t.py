import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import joinedload

from answers.adapters.db.question import Question, User, get_or_create

pytestmark = pytest.mark.anyio


async def test_t(sqlite_memory_session_maker: async_sessionmaker[AsyncSession]):
    async with sqlite_memory_session_maker() as session:
        res = await get_or_create(
            text="rrr",
            question_type="ggg",
            user=User("tttt"),
            option=("1", "2"),
            extra_option=(),
            session=session,
        )
        await session.commit()
        r = await session.execute(
            select(Question)
            .options(
                joinedload(Question.option),
                joinedload(Question.answers),
                joinedload(Question.user),
            )
            .where(
                Question.id == res.id,
            )
            .limit(1)
        )
        print(r.unique().scalars().one())
        assert False
