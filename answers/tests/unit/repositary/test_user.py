import pytest

from answers.domain import commands, models
from answers.domain.abstract.repository import AbstractRepository
from answers.domain.exceptions import repository_exc

pytestmark = pytest.mark.anyio


async def test_create(repository: AbstractRepository, create_user_command: commands.CreateUser):
    user = await repository.create_user(command=create_user_command)
    assert user.user_id.get_secret_value() == create_user_command.user_id

    with pytest.raises(repository_exc.UserAlreadyExist) as error:
        await repository.create_user(command=create_user_command)
        assert error.value.user.id == user.id


async def test_get(repository: AbstractRepository, user_in_db: models.User):
    user = await repository.get_user_by_id(user_id=user_in_db.id)
    assert user == user_in_db

    wrong_user_id = "wrong_id"
    with pytest.raises(repository_exc.UserDoesNotExist) as error:
        await repository.get_user_by_id(user_id=wrong_user_id)
        assert error.value.user_id == wrong_user_id
