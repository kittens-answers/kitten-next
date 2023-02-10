import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from answers.adapters.repository.sql_alchemy import SQLAlchemyQuestionRepository
from answers.domain.commands import CreateQuestion, QuestionType

pytestmark = pytest.mark.anyio


@pytest.fixture
def simple_create_question_dto():
    return CreateQuestion(
        question_text="text",
        question_type=QuestionType.ONE,
    )


async def test_empty_bd(
    sqlite_memory_session_maker: async_sessionmaker[AsyncSession],
    simple_create_question_dto: CreateQuestion,
):
    repo = SQLAlchemyQuestionRepository()
    async with sqlite_memory_session_maker() as session:
        res = await repo.get(dto=simple_create_question_dto, uow=session)
        assert res is None


async def test_create(
    sqlite_memory_session_maker: async_sessionmaker[AsyncSession],
    simple_create_question_dto: CreateQuestion,
):
    user_id = "4"
    repo = SQLAlchemyQuestionRepository()
    async with sqlite_memory_session_maker() as session:
        await repo.create(dto=simple_create_question_dto, user_id=user_id, uow=session)
        await session.commit()
        res = await repo.get(dto=simple_create_question_dto, uow=session)
        assert res is not None
        assert res.created_by == user_id
