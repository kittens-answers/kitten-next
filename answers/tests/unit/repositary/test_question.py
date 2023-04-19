import pytest

from answers.domain import commands, models
from answers.domain.abstract.repository import AbstractRepository
from answers.domain.exceptions import repository_exc

pytestmark = pytest.mark.anyio


async def test_create(
    repository: AbstractRepository,
    user_in_db: models.User,
    create_question_command: commands.CreateQuestion,
):
    question = await repository.create_question(user=user_in_db, command=create_question_command)
    assert isinstance(question, models.Question)


@pytest.mark.usefixtures("question_in_db")
async def test_get(
    repository: AbstractRepository,
    user_in_db: models.User,
    create_question_command: commands.CreateQuestion,
):
    with pytest.raises(repository_exc.QuestionAlreadyExist):
        await repository.create_question(user=user_in_db, command=create_question_command)


async def test_different_text(
    repository: AbstractRepository,
    user_in_db: models.User,
    create_question_command: commands.CreateQuestion,
    question_in_db: models.Question,
):
    create_question_command.question_text = create_question_command.question_text + "diff"
    question = await repository.create_question(user=user_in_db, command=create_question_command)
    assert question_in_db.id != question.id


async def test_different_type(
    repository: AbstractRepository,
    user_in_db: models.User,
    create_question_command: commands.CreateQuestion,
    question_in_db: models.Question,
):
    create_question_command.question_type = models.QuestionType.MANY
    question = await repository.create_question(user=user_in_db, command=create_question_command)
    assert question_in_db.id != question.id


async def test_empty_options(
    repository: AbstractRepository,
    user_in_db: models.User,
    create_question_command: commands.CreateQuestion,
    question_in_db: models.Question,
):
    create_question_command.options = list()
    question = await repository.create_question(user=user_in_db, command=create_question_command)
    assert question_in_db.id != question.id


async def test_get_by_id(
    repository: AbstractRepository,
    question_in_db: models.Question,
):
    question = await repository.get_question_by_id(question_in_db.id)
    assert question == question_in_db

    with pytest.raises(repository_exc.QuestionDoesNotExist):
        await repository.get_question_by_id("not in db")


async def test_with_different_user(
    repository: AbstractRepository,
    create_question_command: commands.CreateQuestion,
    question_in_db: models.Question,
):
    new_user = await repository.create_user(commands.CreateUser(user_id="new user"))
    with pytest.raises(repository_exc.QuestionAlreadyExist) as error:
        await repository.create_question(user=new_user, command=create_question_command)
    assert error.value.question.id == question_in_db.id
    assert error.value.question.created_by != new_user.id


async def test_different_extra_options(
    repository: AbstractRepository, create_question_command: commands.CreateQuestion, user_in_db: models.User
):
    create_question_command.question_type = models.QuestionType.MATCH
    create_question_command.extra_options = ["a", "b"]
    question1 = await repository.create_question(user=user_in_db, command=create_question_command)

    create_question_command.options = []
    create_question_command.extra_options = []
    question2 = await repository.create_question(user=user_in_db, command=create_question_command)

    assert question1.id != question2.id
