import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from answers.adapters.db import BootStrap, DBSettings
from answers.adapters.db.db_models import User
from answers.adapters.repository.sql_alchemy import (
    SQLAlchemyQuestionRepository,
    SQLAlchemyRepository,
)
from answers.domain.commands import CreateAnswer, CreateQuestion
from answers.domain.models import QuestionType

pytestmark = pytest.mark.anyio


@pytest.fixture
async def sqlite_memory_session_maker():
    config = DBSettings(url="sqlite+aiosqlite://", echo=False)
    bootstrap = BootStrap(config=config)
    session = await bootstrap.start()
    yield session
    await bootstrap.stop()


@pytest.fixture
async def sql_repository(sqlite_memory_session_maker: async_sessionmaker[AsyncSession]):
    rep = SQLAlchemyRepository(session_factory=sqlite_memory_session_maker)
    return rep


@pytest.fixture
def test_question_dto():
    return CreateQuestion(
        options=["1", "2"],
        extra_options=["a", "b"],
        question_text="question?",
        question_type=QuestionType.ONE,
    )


@pytest.fixture
def test_answer_dto(question_id: str):
    return CreateAnswer(question_id=question_id, answer=[("1", "true"), ("2", "false")])


@pytest.fixture
async def user_in_db(
    sql_repository: SQLAlchemyRepository,
):
    async with sql_repository:
        user = await sql_repository.users.create(user_id="user_in_db")
        await sql_repository.commit()
    return user


@pytest.fixture
async def question_id(
    sqlite_memory_session_maker: async_sessionmaker[AsyncSession],
    test_question_dto: CreateQuestion,
    user_in_db: User,
):
    async with sqlite_memory_session_maker() as session:
        rep = SQLAlchemyQuestionRepository(session=session)
        question = await rep.create(dto=test_question_dto, user_id=user_in_db.id)
    return question.id
