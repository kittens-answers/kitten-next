import pytest

from answers.adapters.repository import AbstractRepository
from answers.domain.commands import CreateUser
from answers.domain.models import User

pytestmark = pytest.mark.anyio


async def test_empty(repository: AbstractRepository, user_dto: CreateUser):
    async with repository:
        user = await repository.users.get(dto=user_dto)

    assert user is None


async def test_get_if_exist(
    repository: AbstractRepository, user_dto: CreateUser, user_in_db: User
):
    async with repository:
        user = await repository.users.get(dto=user_dto)

    assert user is not None
    assert user.id == user_in_db.id


async def test_get_or_create_empty(
    repository: AbstractRepository, user_dto: CreateUser
):
    async with repository:
        user, is_created = await repository.users.get_or_create(dto=user_dto)
        await repository.commit()

    assert is_created is True
    assert user is not None


async def test_get_or_create_if_exist(
    repository: AbstractRepository, user_dto: CreateUser, user_in_db: User
):
    async with repository:
        user, is_created = await repository.users.get_or_create(dto=user_dto)
        await repository.commit()

    assert is_created is False
    assert user.id == user_in_db.id
