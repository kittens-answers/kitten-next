import pytest
from faker import Faker

from answers.adapters.sqlalchemy.repository import DBSettings, SQLAlchemyRepository
from answers.domain import commands, models
from answers.domain.abstract.repository import AbstractRepository

pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def repository():
    async with SQLAlchemyRepository(
        settings=DBSettings(sqlalchemy_drivername="sqlite+aiosqlite", sqlalchemy_database=None)
    ) as repo:
        yield repo


@pytest.fixture
def create_user_command(faker: Faker):
    return commands.CreateUser(user_id=faker.word())


@pytest.fixture
async def user_in_db(repository: AbstractRepository, create_user_command: commands.CreateUser):
    return await repository.create_user(create_user_command)


@pytest.fixture
def create_question_command(faker: Faker):
    return commands.CreateQuestion(
        question_text=faker.sentence(),
        question_type=commands.QuestionType.ONE,
        options=faker.sentences(),
        extra_options=[],
    )


@pytest.fixture
async def question_in_db(
    repository: AbstractRepository,
    create_question_command: commands.CreateQuestion,
    user_in_db: models.User,
):
    return await repository.create_question(user=user_in_db, command=create_question_command)


@pytest.fixture
def create_answer_command(create_question_command: commands.CreateQuestion):
    answer = [(v, str(False)) for v in create_question_command.options]
    answer[0] = (answer[0][0], str(True))
    return commands.CreateAnswer(answer=answer)


@pytest.fixture
async def answer_in_db(
    create_answer_command: commands.CreateAnswer,
    repository: AbstractRepository,
    user_in_db: models.User,
    question_in_db: models.Question,
):
    return await repository.create_answer(user=user_in_db, question_id=question_in_db.id, command=create_answer_command)


@pytest.fixture
def create_tag_command():
    return commands.CreateTag(tag_name=models.TagsType.IS_CORRECT, value=str(True))


@pytest.fixture
async def tag_in_db(
    create_tag_command: commands.CreateTag,
    repository: AbstractRepository,
    user_in_db: models.User,
    answer_in_db: models.Answer,
):
    return await repository.add_tag(user=user_in_db, answer_id=answer_in_db.id, command=create_tag_command)
