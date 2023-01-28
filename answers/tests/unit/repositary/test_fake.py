import pytest

from answers.adapters.repository import FakeQuestionRepository, FakeOptionsRepository
from answers.domain.models import QuestionType, Options, Question
from answers.service_layer.unit_of_work import FakeUOW

pytestmark = pytest.mark.anyio


async def test_add_question():
    rep = FakeQuestionRepository()
    uow = FakeUOW()
    question = Question(
        user_id="1", question_text="text", question_type=QuestionType.ONE
    )
    res = await rep.add(question=question, uof=uow)

    assert rep._data[res] == question

    res2 = await rep.add(question=question, uof=uow)

    assert res == res2
    assert len(rep._data) == 1


async def test_add_options():
    rep = FakeOptionsRepository()
    uow = FakeUOW()
    options = Options(
        options=frozenset(("a", "b")), extra_options=frozenset(("1", "2"))
    )
    res = await rep.add(options=options, uow=uow)

    assert rep._data[res] == options

    res2 = await rep.add(options=options, uow=uow)

    assert res == res2
    assert len(rep._data) == 1

    options2 = Options(
        options=frozenset(("b", "a")), extra_options=frozenset(("1", "2"))
    )
    assert options2 == options
    res3 = await rep.add(options=options2, uow=uow)
    assert res3 == res
