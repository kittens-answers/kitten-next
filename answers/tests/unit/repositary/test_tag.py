import pytest

from answers.adapters.repository import AbstractRepository
from answers.domain.commands import CreateTag
from answers.domain.models import AnswerTag

pytestmark = pytest.mark.anyio


async def test_empty(repository: AbstractRepository, tag_dto: CreateTag):
    async with repository:
        tag = await repository.tags.get(dto=tag_dto)

    assert tag is None


async def test_get_if_exist(
    repository: AbstractRepository, tag_dto: CreateTag, tag_in_db: AnswerTag
):
    async with repository:
        tag = await repository.tags.get(dto=tag_dto)

    assert tag is not None
    assert tag.id == tag_in_db.id


async def test_update_empty(repository: AbstractRepository, tag_dto: CreateTag):
    async with repository:
        tag = await repository.tags.create_or_update(dto=tag_dto)

    assert tag is not None


async def test_update_if_exist(
    repository: AbstractRepository, tag_dto: CreateTag, tag_in_db: AnswerTag
):
    old_value = tag_dto.value
    tag_dto.value = old_value + "new"

    async with repository:
        tag = await repository.tags.create_or_update(dto=tag_dto)

    assert tag.id == tag_in_db.id
    assert tag.value != old_value
