import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from answers.adapters.db.db_models import User
from answers.domain.commands import CreateAnswer
from answers.adapters.repository.sql_alchemy import SQLAlchemyAnswerRepository


pytestmark = pytest.mark.anyio


async def test_empty(
    sqlite_memory_session_maker: async_sessionmaker[AsyncSession],
    test_answer_dto: CreateAnswer,
):
    async with sqlite_memory_session_maker() as session:
        rep = SQLAlchemyAnswerRepository(session=session)
        res = await rep.get(dto=test_answer_dto)
        assert res is None


async def test_exist(
    sqlite_memory_session_maker: async_sessionmaker[AsyncSession],
    test_answer_dto: CreateAnswer,
    user_in_db: User,
):
    async with sqlite_memory_session_maker() as session:
        rep = SQLAlchemyAnswerRepository(session=session)
        answer_in_db = await rep.create(dto=test_answer_dto, user_id=user_in_db.id)
        res = await rep.get(dto=test_answer_dto)
        assert res is not None
        assert res.answer_id == answer_in_db.answer_id


async def test_exist_reverse(
    sqlite_memory_session_maker: async_sessionmaker[AsyncSession],
    test_answer_dto: CreateAnswer,
    user_in_db: User,
):
    async with sqlite_memory_session_maker() as session:
        rep = SQLAlchemyAnswerRepository(session=session)
        answer_in_db = await rep.create(dto=test_answer_dto, user_id=user_in_db.id)
        test_answer_dto.answer.reverse()
        res = await rep.get(dto=test_answer_dto)
        print(res)
        assert res is not None
        assert res.answer_id == answer_in_db.answer_id


async def test_get_or_create_twice(
    sqlite_memory_session_maker: async_sessionmaker[AsyncSession],
    test_answer_dto: CreateAnswer,
    user_in_db: User,
):
    async with sqlite_memory_session_maker() as session:
        rep = SQLAlchemyAnswerRepository(session=session)
        a1 = await rep.get_or_create(dto=test_answer_dto, user_id=user_in_db.id)
        a2 = await rep.get_or_create(
            dto=test_answer_dto,
            user_id=user_in_db.id,
        )
        assert a1.answer_id == a2.answer_id
