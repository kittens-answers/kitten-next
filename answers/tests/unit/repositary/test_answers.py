import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from answers.adapters.db.db_models import User
from answers.adapters.db.answer import get, create, get_or_create
from answers.domain.commands import CreateAnswer


pytestmark = pytest.mark.anyio


async def test_empty(
    sqlite_memory_session_maker: async_sessionmaker[AsyncSession],
    test_answer_dto: CreateAnswer,
):
    async with sqlite_memory_session_maker() as session:
        res = await get(dto=test_answer_dto, session=session)
        assert res is None


async def test_exist(
    sqlite_memory_session_maker: async_sessionmaker[AsyncSession],
    test_answer_dto: CreateAnswer,
    user_in_db: User,
):
    async with sqlite_memory_session_maker() as session:
        answer_in_db = await create(
            dto=test_answer_dto, user_id=user_in_db.id, session=session
        )
        res = await get(dto=test_answer_dto, session=session)
        assert res is not None
        assert res.id == answer_in_db.id


async def test_exist_reverse(
    sqlite_memory_session_maker: async_sessionmaker[AsyncSession],
    test_answer_dto: CreateAnswer,
    user_in_db: User,
):
    async with sqlite_memory_session_maker() as session:
        answer_in_db = await create(
            dto=test_answer_dto, user_id=user_in_db.id, session=session
        )
        test_answer_dto.answer.reverse()
        res = await get(dto=test_answer_dto, session=session)
        assert res is not None
        assert res.id == answer_in_db.id


async def test_get_or_create_twice(
    sqlite_memory_session_maker: async_sessionmaker[AsyncSession],
    test_answer_dto: CreateAnswer,
    user_in_db: User,
):
    async with sqlite_memory_session_maker() as session:
        a1 = await get_or_create(
            dto=test_answer_dto, user_id=user_in_db.id, session=session
        )
        a2 = await get_or_create(
            dto=test_answer_dto, user_id=user_in_db.id, session=session
        )
        assert a1.id == a2.id
