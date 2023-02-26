import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from answers.adapters.db.db_models import User
from answers.domain.commands import CreateQuestion
from answers.domain.models import QuestionType
from answers.domain.specification import TextContains
from answers.adapters.repository.sql_alchemy import SQLAlchemyQuestionRepository
from sqlalchemy.exc import IntegrityError

pytestmark = pytest.mark.anyio


async def test_empty(
    sqlite_memory_session_maker: async_sessionmaker[AsyncSession],
    test_question_dto: CreateQuestion,
):
    async with sqlite_memory_session_maker() as session:
        rep = SQLAlchemyQuestionRepository(session=session)
        res = await rep.get(dto=test_question_dto)
        assert res is None


async def test_exist(
    sqlite_memory_session_maker: async_sessionmaker[AsyncSession],
    test_question_dto: CreateQuestion,
    user_in_db: User,
):
    async with sqlite_memory_session_maker() as session:
        rep = SQLAlchemyQuestionRepository(session=session)
        question_dto_in_db = await rep.create(
            dto=test_question_dto, user_id=user_in_db.id
        )
        res = await rep.get(dto=test_question_dto)
        assert res is not None
        assert res.id == question_dto_in_db.id


async def test_exist_reverse(
    sqlite_memory_session_maker: async_sessionmaker[AsyncSession],
    test_question_dto: CreateQuestion,
    user_in_db: User,
):
    async with sqlite_memory_session_maker() as session:
        rep = SQLAlchemyQuestionRepository(session=session)
        question_dto_in_db = await rep.create(
            dto=test_question_dto, user_id=user_in_db.id
        )
        test_question_dto.options.reverse()
        res = await rep.get(dto=test_question_dto)
        assert res is not None
        assert res.id == question_dto_in_db.id


async def test_exist_with_extra(
    sqlite_memory_session_maker: async_sessionmaker[AsyncSession],
    test_question_dto: CreateQuestion,
    user_in_db: User,
):
    async with sqlite_memory_session_maker() as session:
        rep = SQLAlchemyQuestionRepository(session=session)
        await rep.create(dto=test_question_dto, user_id=user_in_db.id)
        test_question_dto.options.append("3")
        test_question_dto.extra_options.append("c")
        res = await rep.get(dto=test_question_dto)
        assert res is None


async def test_exist_same_size(
    sqlite_memory_session_maker: async_sessionmaker[AsyncSession],
    test_question_dto: CreateQuestion,
    user_in_db: User,
):
    async with sqlite_memory_session_maker() as session:
        rep = SQLAlchemyQuestionRepository(session=session)
        await rep.create(dto=test_question_dto, user_id=user_in_db.id)
        test_question_dto.options[0] = "4"
        test_question_dto.extra_options[0] = "c"
        res = await rep.get(dto=test_question_dto)
        assert res is None


async def test_exist_different_question(
    sqlite_memory_session_maker: async_sessionmaker[AsyncSession],
    test_question_dto: CreateQuestion,
    user_in_db: User,
):
    async with sqlite_memory_session_maker() as session:
        rep = SQLAlchemyQuestionRepository(session=session)
        await rep.create(dto=test_question_dto, user_id=user_in_db.id)
        test_question_dto.question_text = "different_question"
        res = await rep.get(
            dto=test_question_dto,
        )
        assert res is None


async def test_exist_different_question_type(
    sqlite_memory_session_maker: async_sessionmaker[AsyncSession],
    test_question_dto: CreateQuestion,
    user_in_db: User,
):
    async with sqlite_memory_session_maker() as session:
        rep = SQLAlchemyQuestionRepository(session=session)
        await rep.create(dto=test_question_dto, user_id=user_in_db.id)
        test_question_dto.question_type = QuestionType.MANY
        res = await rep.get(dto=test_question_dto)
        assert res is None


async def test_get_or_create_twice(
    sqlite_memory_session_maker: async_sessionmaker[AsyncSession],
    test_question_dto: CreateQuestion,
    user_in_db: User,
):
    async with sqlite_memory_session_maker() as session:
        rep = SQLAlchemyQuestionRepository(session=session)
        q1 = await rep.get_or_create(dto=test_question_dto, user_id=user_in_db.id)
        q2 = await rep.get_or_create(dto=test_question_dto, user_id="new user id")

        assert q1.id == q2.id
        assert q1.created_by == q2.created_by


async def test_list(
    sqlite_memory_session_maker: async_sessionmaker[AsyncSession],
    test_question_dto: CreateQuestion,
    user_in_db: User,
):
    async with sqlite_memory_session_maker() as session:
        rep = SQLAlchemyQuestionRepository(session=session)
        assert len(await rep.list([])) == 0
        q1 = await rep.get_or_create(dto=test_question_dto, user_id=user_in_db.id)
        q_list = await rep.list([TextContains(q=test_question_dto.question_text[:1])])
        assert len(q_list) == 1
        assert q_list[0].id == q1.id


async def test_unique(
    sqlite_memory_session_maker: async_sessionmaker[AsyncSession],
    test_question_dto: CreateQuestion,
    user_in_db: User,
):
    async with sqlite_memory_session_maker() as session:
        rep = SQLAlchemyQuestionRepository(session=session)
        await rep.create(dto=test_question_dto, user_id=user_in_db.id)
        with pytest.raises(IntegrityError):
            await rep.create(dto=test_question_dto, user_id=user_in_db.id)
