import pytest

from answers.adapters.db.db_models import User
from answers.adapters.repository import AbstractRepository
from answers.domain.commands import CreateAnswer

pytestmark = pytest.mark.anyio


async def test_empty(
    test_answer_dto: CreateAnswer,
    sql_repository: AbstractRepository,
):
    async with sql_repository:
        res = await sql_repository.answers.get(dto=test_answer_dto)
        await sql_repository.commit()

    assert res is None


async def test_exist(
    sql_repository: AbstractRepository,
    test_answer_dto: CreateAnswer,
    user_in_db: User,
):
    async with sql_repository:
        answer_in_db = await sql_repository.answers.create(
            dto=test_answer_dto, user_id=user_in_db.id
        )
        await sql_repository.commit()

        res = await sql_repository.answers.get(dto=test_answer_dto)

    assert res is not None
    assert res.answer_id == answer_in_db.answer_id


async def test_exist_reverse(
    sql_repository: AbstractRepository,
    test_answer_dto: CreateAnswer,
    user_in_db: User,
):
    async with sql_repository:
        answer_in_db = await sql_repository.answers.create(
            dto=test_answer_dto, user_id=user_in_db.id
        )
        await sql_repository.commit()

        test_answer_dto.answer.reverse()
        res = await sql_repository.answers.get(dto=test_answer_dto)

    assert res is not None
    assert res.answer_id == answer_in_db.answer_id


async def test_get_or_create_twice(
    sql_repository: AbstractRepository,
    test_answer_dto: CreateAnswer,
    user_in_db: User,
):
    async with sql_repository:
        a1 = await sql_repository.answers.get_or_create(
            dto=test_answer_dto, user_id=user_in_db.id
        )
        await sql_repository.commit()
        a2 = await sql_repository.answers.get_or_create(
            dto=test_answer_dto,
            user_id=user_in_db.id,
        )
        assert a1.answer_id == a2.answer_id
