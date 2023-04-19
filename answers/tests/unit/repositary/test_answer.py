import pytest

from answers.domain import commands, models
from answers.domain.abstract.repository import AbstractRepository
from answers.domain.exceptions import repository_exc

pytestmark = pytest.mark.anyio


async def test_get_by_id_if_not_exist(
    repository: AbstractRepository,
):
    with pytest.raises(repository_exc.AnswerDoesNotExist):
        await repository.get_answer_by_id("wrong")


async def test_get_by_id_if_exist(repository: AbstractRepository, answer_in_db: models.Answer):
    answer = await repository.get_answer_by_id(answer_in_db.id)
    assert answer == answer_in_db


async def test_create_answer(
    repository: AbstractRepository,
    user_in_db: models.User,
    create_answer_command: commands.CreateAnswer,
    question_in_db: models.Question,
):
    answer = await repository.create_answer(
        user=user_in_db, question_id=question_in_db.id, command=create_answer_command
    )
    assert answer == await repository.get_answer_by_id(answer.id)


async def test_create_answer_with_incorrect_question_id(
    repository: AbstractRepository,
    user_in_db: models.User,
    create_answer_command: commands.CreateAnswer,
):
    with pytest.raises(repository_exc.QuestionDoesNotExist):
        await repository.create_answer(user=user_in_db, question_id="wrong", command=create_answer_command)


async def test_reversed_answer(
    repository: AbstractRepository,
    user_in_db: models.User,
    create_answer_command: commands.CreateAnswer,
    answer_in_db: models.Answer,
    question_in_db: models.Question,
):
    create_answer_command.answer.reverse()
    with pytest.raises(repository_exc.AnswerAlreadyExist) as error:
        await repository.create_answer(user=user_in_db, question_id=question_in_db.id, command=create_answer_command)
        assert error.value.answer == answer_in_db


async def test_wrong_question_id(
    repository: AbstractRepository,
    user_in_db: models.User,
    create_answer_command: commands.CreateAnswer,
):
    with pytest.raises(repository_exc.QuestionDoesNotExist):
        await repository.create_answer(user=user_in_db, question_id="wrong", command=create_answer_command)


@pytest.mark.parametrize("is_correct", [True, False])
async def test_create_tag(
    repository: AbstractRepository,
    user_in_db: models.User,
    create_answer_command: commands.CreateAnswer,
    is_correct: bool,
    question_in_db: models.Question,
):
    create_answer_command.is_correct = is_correct
    answer = await repository.create_answer(
        user=user_in_db, question_id=question_in_db.id, command=create_answer_command
    )
    assert answer.tags[0].tag_name == models.TagsType.IS_CORRECT
    assert answer.tags[0].value == str(is_correct)
