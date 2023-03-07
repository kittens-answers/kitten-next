import pytest

from answers.adapters.repository import AbstractRepository
from answers.domain.commands import CreateTag
from answers.domain.models import AnswerTag

pytestmark = pytest.mark.anyio


async def test_empty(repository: AbstractRepository, tag_dto: CreateTag):
    async with repository:
        tag = await repository.tags.get(dto=tag_dto)
        await repository.commit()

    assert tag is None


async def test_get_if_exist(
    repository: AbstractRepository, tag_dto: CreateTag, tag_in_db: AnswerTag
):
    async with repository:
        tag = await repository.tags.get(dto=tag_dto)
        await repository.commit()

    assert tag is not None
    assert tag.id == tag_in_db.id


async def test_update_empty(repository: AbstractRepository, tag_dto: CreateTag):
    async with repository:
        tag, is_created = await repository.tags.get_or_create(dto=tag_dto)
        await repository.commit()

    assert is_created is True
    assert tag is not None


async def test_update_if_exist(
    repository: AbstractRepository, tag_dto: CreateTag, tag_in_db: AnswerTag
):
    async with repository:
        tag, is_created = await repository.tags.get_or_create(dto=tag_dto)
        await repository.commit()

    assert is_created is False
    assert tag.id == tag_in_db.id
