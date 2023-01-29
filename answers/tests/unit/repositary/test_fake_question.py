import pytest

from answers.adapters.repository import FakeQuestionRepository
from answers.domain.models import Question
from answers.service_layer.unit_of_work import FakeUOW

pytestmark = pytest.mark.anyio


async def test_add_question_if_not_exist(
    question_one: Question, fake_question_rep: FakeQuestionRepository, fake_uow: FakeUOW
):
    assert len(fake_question_rep._data) == 0

    question_id = await fake_question_rep.add(question=question_one, uof=fake_uow)

    assert fake_question_rep._data[question_id] == question_one
    assert len(fake_question_rep._data) == 1


async def test_add_question_if_exist(
    question_one: Question,
    fake_question_rep: FakeQuestionRepository,
    fake_uow: FakeUOW,
    question_one_in_db: str,
):
    assert len(fake_question_rep._data) == 1

    new_id = await fake_question_rep.add(question=question_one, uof=fake_uow)

    assert fake_question_rep._data[new_id] == question_one
    assert len(fake_question_rep._data) == 1
    assert new_id == question_one_in_db
