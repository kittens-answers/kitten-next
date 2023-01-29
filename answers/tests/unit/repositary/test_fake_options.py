import pytest

from answers.adapters.repository import FakeOptionsRepository
from answers.domain.models import Options
from answers.service_layer.unit_of_work import FakeUOW

pytestmark = pytest.mark.anyio


async def test_add_options_if_not_exist(
    fake_options_repository: FakeOptionsRepository,
    fake_uow: FakeUOW,
    options_one: Options,
):
    assert len(fake_options_repository._data) == 0
    res = await fake_options_repository.add(options=options_one, uow=fake_uow)

    assert fake_options_repository._data[res] == options_one
    assert len(fake_options_repository._data) == 1


async def test_add_options_if_exist(
    fake_options_repository: FakeOptionsRepository,
    fake_uow: FakeUOW,
    options_one: Options,
    options_one_in_db: str,
):
    assert len(fake_options_repository._data) == 1
    new_id = await fake_options_repository.add(options=options_one, uow=fake_uow)

    assert fake_options_repository._data[new_id] == options_one
    assert len(fake_options_repository._data) == 1
    assert new_id == options_one_in_db


async def test_add_options_if_exist_variant(
    fake_options_repository: FakeOptionsRepository,
    fake_uow: FakeUOW,
    options_one_variant: Options,
    options_one_in_db: str,
):
    assert len(fake_options_repository._data) == 1
    new_id = await fake_options_repository.add(
        options=options_one_variant, uow=fake_uow
    )

    assert fake_options_repository._data[new_id] == options_one_variant
    assert len(fake_options_repository._data) == 1
    assert new_id == options_one_in_db
