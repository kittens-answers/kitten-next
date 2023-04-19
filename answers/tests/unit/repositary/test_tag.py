import pytest

from answers.domain import commands, models
from answers.domain.abstract.repository import AbstractRepository
from answers.domain.exceptions import repository_exc

pytestmark = pytest.mark.anyio


async def test_wrong_answer_id(
    repository: AbstractRepository,
    create_tag_command: commands.CreateTag,
    user_in_db: models.User,
):
    with pytest.raises(repository_exc.AnswerDoesNotExist):
        await repository.add_tag(user=user_in_db, answer_id="wrong", command=create_tag_command)


async def test_create(
    repository: AbstractRepository,
    create_tag_command: commands.CreateTag,
    user_in_db: models.User,
    answer_in_db: models.Answer,
):
    tag1 = await repository.add_tag(user=user_in_db, answer_id=answer_in_db.id, command=create_tag_command)
    assert tag1.value == create_tag_command.value

    tag2 = await repository.add_tag(user=user_in_db, answer_id=answer_in_db.id, command=create_tag_command)
    assert tag2.value == create_tag_command.value

    create_tag_command.value = str(False)
    tag3 = await repository.add_tag(user=user_in_db, answer_id=answer_in_db.id, command=create_tag_command)
    assert tag3.value == create_tag_command.value

    assert tag1.id == tag2.id
    assert tag1.id == tag3.id
