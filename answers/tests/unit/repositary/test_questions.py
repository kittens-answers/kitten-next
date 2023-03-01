import pytest
from sqlalchemy.exc import IntegrityError

from answers.adapters.repository import AbstractRepository
from answers.domain.commands import CreateQuestion
from answers.domain.models import Question, QuestionType
from answers.domain.specifications import TextContains

pytestmark = pytest.mark.anyio


async def test_empty(
    repository: AbstractRepository,
    question_dto: CreateQuestion,
):
    async with repository:
        res = await repository.questions.get(dto=question_dto)
        await repository.commit()

    assert res is None


async def test_exist(
    repository: AbstractRepository,
    question_dto: CreateQuestion,
    question_in_db: Question,
):
    async with repository:
        res = await repository.questions.get(dto=question_dto)

    assert res is not None
    assert res.id == question_in_db.id


async def test_exist_reverse(
    repository: AbstractRepository,
    question_dto: CreateQuestion,
    question_in_db: Question,
):
    async with repository:
        question_dto.options.reverse()
        res = await repository.questions.get(dto=question_dto)

    assert res is not None
    assert res.id == question_in_db.id


@pytest.mark.usefixtures("question_in_db")
async def test_exist_with_extra(
    repository: AbstractRepository,
    question_dto: CreateQuestion,
):
    async with repository:
        question_dto.options.append("3")
        question_dto.extra_options.append("c")
        res = await repository.questions.get(dto=question_dto)

    assert res is None


@pytest.mark.usefixtures("question_in_db")
async def test_exist_same_size(
    repository: AbstractRepository,
    question_dto: CreateQuestion,
):
    async with repository:
        question_dto.options[0] = "4"
        question_dto.extra_options[0] = "c"
        res = await repository.questions.get(dto=question_dto)

    assert res is None


@pytest.mark.usefixtures("question_in_db")
async def test_exist_different_question(
    repository: AbstractRepository,
    question_dto: CreateQuestion,
):
    async with repository:
        question_dto.question_text = "different_question"
        res = await repository.questions.get(
            dto=question_dto,
        )

    assert res is None


@pytest.mark.usefixtures("question_in_db")
async def test_exist_different_question_type(
    repository: AbstractRepository,
    question_dto: CreateQuestion,
):
    async with repository:
        question_dto.question_type = QuestionType.MANY
        res = await repository.questions.get(dto=question_dto)

    assert res is None


async def test_get_or_create_twice(
    repository: AbstractRepository,
    question_dto: CreateQuestion,
    question_in_db: Question,
):
    async with repository:
        question = await repository.questions.get_or_create(dto=question_dto)
        await repository.commit()

    assert question_in_db.id == question.id
    assert question_in_db.created_by == question.created_by


async def test_list(
    repository: AbstractRepository,
    question_dto: CreateQuestion,
):
    async with repository:
        assert len(await repository.questions.list([])) == 0
        q1 = await repository.questions.get_or_create(dto=question_dto)
        await repository.commit()

        q_list = await repository.questions.list(
            [TextContains(q=question_dto.question_text[:1])]
        )

    assert len(q_list) == 1
    assert q_list[0].id == q1.id


@pytest.mark.usefixtures("question_in_db")
async def test_unique(
    repository: AbstractRepository,
    question_dto: CreateQuestion,
):
    async with repository:
        with pytest.raises(expected_exception=IntegrityError):
            await repository.questions.create(dto=question_dto)
