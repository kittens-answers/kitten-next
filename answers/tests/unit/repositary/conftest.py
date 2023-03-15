import pytest

from answers.adapters.sqlalchemy.repository import SQLAlchemyRepository
from answers.domain.commands import CreateAnswer, CreateQuestion, CreateTag, CreateUser
from answers.domain.models import (
    Answer,
    AnswerTag,
    Question,
    QuestionType,
    TagsType,
    User,
)

pytestmark = pytest.mark.anyio


@pytest.fixture
def question_dto(user_in_db: User) -> CreateQuestion:
    return CreateQuestion(
        options=["1", "2"],
        extra_options=["a", "b"],
        question_text="question?",
        question_type=QuestionType.ONE,
        user_id=user_in_db.id,
    )


@pytest.fixture
async def question_in_db(
    repository: SQLAlchemyRepository,
    question_dto: CreateQuestion,
) -> Question:
    async with repository:
        question = await repository.questions.create(dto=question_dto)
        await repository.commit()
    return question


@pytest.fixture
def answer_dto(
    question_in_db: Question,
    user_in_db: User,
) -> CreateAnswer:
    return CreateAnswer(
        question_id=question_in_db.id,
        answer=[("1", "true"), ("2", "false")],
        user_id=user_in_db.id,
    )


@pytest.fixture
async def answer_in_db(
    repository: SQLAlchemyRepository, answer_dto: CreateAnswer
) -> Answer:
    async with repository:
        answer = await repository.answers.create(dto=answer_dto)
        await repository.commit()
    return answer


@pytest.fixture
def user_dto() -> CreateUser:
    return CreateUser(user_id="user_in_db")


@pytest.fixture
async def user_in_db(repository: SQLAlchemyRepository, user_dto: CreateUser) -> User:
    async with repository:
        user = await repository.users.create(dto=user_dto)
        await repository.commit()
    return user


@pytest.fixture
def tag_dto(answer_in_db: Answer) -> CreateTag:
    return CreateTag(
        answer_id=answer_in_db.id,
        user_id=answer_in_db.created_by,
        tag_name=TagsType.IS_CORRECT,
        value=str(True),
    )


@pytest.fixture
async def tag_in_db(repository: SQLAlchemyRepository, tag_dto: CreateTag) -> AnswerTag:
    async with repository:
        tag = await repository.tags.create(dto=tag_dto)
        await repository.commit()
    return tag
