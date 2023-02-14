import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from answers.adapters.db.db_models import User
from answers.adapters.db.question import create, get, get_or_create
from answers.domain.commands import CreateQuestion
from answers.domain.models import QuestionType

pytestmark = pytest.mark.anyio


async def test_empty(
    sqlite_memory_session_maker: async_sessionmaker[AsyncSession],
    test_question_dto: CreateQuestion,
):
    async with sqlite_memory_session_maker() as session:
        res = await get(dto=test_question_dto, session=session)
        assert res is None


async def test_exist(
    sqlite_memory_session_maker: async_sessionmaker[AsyncSession],
    test_question_dto: CreateQuestion,
    user_in_db: User,
):
    async with sqlite_memory_session_maker() as session:
        question_dto_in_db = await create(
            dto=test_question_dto, user_id=user_in_db.id, session=session
        )
        res = await get(dto=test_question_dto, session=session)
        assert res is not None
        assert res.id == question_dto_in_db.id


async def test_exist_reverse(
    sqlite_memory_session_maker: async_sessionmaker[AsyncSession],
    test_question_dto: CreateQuestion,
    user_in_db: User,
):
    async with sqlite_memory_session_maker() as session:
        question_dto_in_db = await create(
            dto=test_question_dto, user_id=user_in_db.id, session=session
        )
        test_question_dto.options.reverse()
        res = await get(dto=test_question_dto, session=session)
        assert res is not None
        assert res.id == question_dto_in_db.id


async def test_exist_with_extra(
    sqlite_memory_session_maker: async_sessionmaker[AsyncSession],
    test_question_dto: CreateQuestion,
    user_in_db: User,
):
    async with sqlite_memory_session_maker() as session:
        await create(dto=test_question_dto, user_id=user_in_db.id, session=session)
        test_question_dto.options.append("3")
        test_question_dto.extra_options.append("c")
        res = await get(dto=test_question_dto, session=session)
        assert res is None


async def test_exist_same_size(
    sqlite_memory_session_maker: async_sessionmaker[AsyncSession],
    test_question_dto: CreateQuestion,
    user_in_db: User,
):

    async with sqlite_memory_session_maker() as session:
        await create(dto=test_question_dto, user_id=user_in_db.id, session=session)
        test_question_dto.options[0] = "4"
        test_question_dto.extra_options[0] = "c"
        res = await get(dto=test_question_dto, session=session)
        assert res is None


async def test_exist_different_question(
    sqlite_memory_session_maker: async_sessionmaker[AsyncSession],
    test_question_dto: CreateQuestion,
    user_in_db: User,
):
    async with sqlite_memory_session_maker() as session:
        await create(dto=test_question_dto, user_id=user_in_db.id, session=session)
        test_question_dto.question_text = "different_question"
        res = await get(dto=test_question_dto, session=session)
        assert res is None


async def test_exist_different_question_type(
    sqlite_memory_session_maker: async_sessionmaker[AsyncSession],
    test_question_dto: CreateQuestion,
    user_in_db: User,
):
    async with sqlite_memory_session_maker() as session:
        await create(dto=test_question_dto, user_id=user_in_db.id, session=session)
        test_question_dto.question_type = QuestionType.MANY
        res = await get(dto=test_question_dto, session=session)
        assert res is None


async def test_get_or_create_twice(
    sqlite_memory_session_maker: async_sessionmaker[AsyncSession],
    test_question_dto: CreateQuestion,
    user_in_db: User,
):
    async with sqlite_memory_session_maker() as session:
        q1 = await get_or_create(
            dto=test_question_dto, user_id=user_in_db.id, session=session
        )
        q2 = await get_or_create(
            dto=test_question_dto, user_id="new user id", session=session
        )

        assert q1.id == q2.id
        assert q1.created_by == q2.created_by
