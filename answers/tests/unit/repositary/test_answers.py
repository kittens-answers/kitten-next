import pytest

from answers.adapters.repository import AbstractRepository
from answers.domain.commands import CreateAnswer
from answers.domain.models import Answer

pytestmark = pytest.mark.anyio


async def test_empty(
    answer_dto: CreateAnswer,
    repository: AbstractRepository,
):
    async with repository:
        res = await repository.answers.get(dto=answer_dto)
        await repository.commit()

    assert res is None


async def test_exist(
    repository: AbstractRepository,
    answer_dto: CreateAnswer,
    answer_in_db: Answer,
):
    async with repository:
        res = await repository.answers.get(dto=answer_dto)

    assert res is not None
    assert res.id == answer_in_db.id


async def test_exist_reverse(
    repository: AbstractRepository,
    answer_dto: CreateAnswer,
    answer_in_db: Answer,
):
    async with repository:
        answer_dto.answer.reverse()
        res = await repository.answers.get(dto=answer_dto)

    assert res is not None
    assert res.id == answer_in_db.id


async def test_get_or_create_if_exist(
    repository: AbstractRepository,
    answer_dto: CreateAnswer,
    answer_in_db: Answer,
):
    async with repository:
        answer, is_created = await repository.answers.get_or_create(dto=answer_dto)
        await repository.commit()

    assert is_created is False
    assert answer_in_db.id == answer.id


async def test_get_or_create_empty(
    repository: AbstractRepository,
    answer_dto: CreateAnswer,
):
    async with repository:
        answer, is_created = await repository.answers.get_or_create(dto=answer_dto)
        await repository.commit()

    assert is_created is True
    assert answer is not None
