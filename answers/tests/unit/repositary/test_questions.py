import pytest
from sqlalchemy.exc import IntegrityError

from answers.adapters.db.db_models import User
from answers.adapters.repository import AbstractRepository
from answers.domain.commands import CreateQuestion
from answers.domain.models import QuestionType
from answers.domain.specification import TextContains

pytestmark = pytest.mark.anyio


async def test_empty(
    sql_repository: AbstractRepository,
    test_question_dto: CreateQuestion,
):
    async with sql_repository:
        res = await sql_repository.questions.get(dto=test_question_dto)
        await sql_repository.commit()

    assert res is None


async def test_exist(
    sql_repository: AbstractRepository,
    test_question_dto: CreateQuestion,
    user_in_db: User,
):
    async with sql_repository:
        question_dto_in_db = await sql_repository.questions.create(
            dto=test_question_dto, user_id=user_in_db.id
        )
        await sql_repository.commit()
        res = await sql_repository.questions.get(dto=test_question_dto)

    assert res is not None
    assert res.id == question_dto_in_db.id


async def test_exist_reverse(
    sql_repository: AbstractRepository,
    test_question_dto: CreateQuestion,
    user_in_db: User,
):
    async with sql_repository:
        question_dto_in_db = await sql_repository.questions.create(
            dto=test_question_dto, user_id=user_in_db.id
        )
        await sql_repository.commit()
        test_question_dto.options.reverse()
        res = await sql_repository.questions.get(dto=test_question_dto)

    assert res is not None
    assert res.id == question_dto_in_db.id


async def test_exist_with_extra(
    sql_repository: AbstractRepository,
    test_question_dto: CreateQuestion,
    user_in_db: User,
):
    async with sql_repository:
        await sql_repository.questions.create(
            dto=test_question_dto, user_id=user_in_db.id
        )
        await sql_repository.commit()

        test_question_dto.options.append("3")
        test_question_dto.extra_options.append("c")
        res = await sql_repository.questions.get(dto=test_question_dto)

    assert res is None


async def test_exist_same_size(
    sql_repository: AbstractRepository,
    test_question_dto: CreateQuestion,
    user_in_db: User,
):
    async with sql_repository:
        await sql_repository.questions.create(
            dto=test_question_dto, user_id=user_in_db.id
        )
        await sql_repository.commit()

        test_question_dto.options[0] = "4"
        test_question_dto.extra_options[0] = "c"
        res = await sql_repository.questions.get(dto=test_question_dto)

    assert res is None


async def test_exist_different_question(
    sql_repository: AbstractRepository,
    test_question_dto: CreateQuestion,
    user_in_db: User,
):
    async with sql_repository:
        await sql_repository.questions.create(
            dto=test_question_dto, user_id=user_in_db.id
        )
        await sql_repository.commit()

        test_question_dto.question_text = "different_question"
        res = await sql_repository.questions.get(
            dto=test_question_dto,
        )

    assert res is None


async def test_exist_different_question_type(
    sql_repository: AbstractRepository,
    test_question_dto: CreateQuestion,
    user_in_db: User,
):
    async with sql_repository:
        await sql_repository.questions.create(
            dto=test_question_dto, user_id=user_in_db.id
        )
        await sql_repository.commit()

        test_question_dto.question_type = QuestionType.MANY
        res = await sql_repository.questions.get(dto=test_question_dto)

    assert res is None


async def test_get_or_create_twice(
    sql_repository: AbstractRepository,
    test_question_dto: CreateQuestion,
    user_in_db: User,
):
    async with sql_repository:
        q1 = await sql_repository.questions.get_or_create(
            dto=test_question_dto, user_id=user_in_db.id
        )
        await sql_repository.commit()
        q2 = await sql_repository.questions.get_or_create(
            dto=test_question_dto, user_id="new user id"
        )
        await sql_repository.commit()

    assert q1.id == q2.id
    assert q1.created_by == q2.created_by


async def test_list(
    sql_repository: AbstractRepository,
    test_question_dto: CreateQuestion,
    user_in_db: User,
):
    async with sql_repository:
        assert len(await sql_repository.questions.list([])) == 0
        q1 = await sql_repository.questions.get_or_create(
            dto=test_question_dto, user_id=user_in_db.id
        )
        await sql_repository.commit()

        q_list = await sql_repository.questions.list(
            [TextContains(q=test_question_dto.question_text[:1])]
        )

    assert len(q_list) == 1
    assert q_list[0].id == q1.id


async def test_unique(
    sql_repository: AbstractRepository,
    test_question_dto: CreateQuestion,
    user_in_db: User,
):
    async with sql_repository:
        await sql_repository.questions.create(
            dto=test_question_dto, user_id=user_in_db.id
        )
        await sql_repository.commit()

        with pytest.raises(expected_exception=IntegrityError):
            await sql_repository.questions.create(
                dto=test_question_dto, user_id=user_in_db.id
            )
