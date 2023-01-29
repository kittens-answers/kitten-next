import pytest

from answers.adapters.repository import FakeOptionsRepository, FakeQuestionRepository
from answers.domain.models import Options, Question, QuestionType
from answers.service_layer.unit_of_work import FakeUOW

pytestmark = pytest.mark.anyio


@pytest.fixture
def fake_options_repository():
    return FakeOptionsRepository()


@pytest.fixture
def fake_uow():
    return FakeUOW()


@pytest.fixture
def options_one():
    return Options(options=frozenset(("a", "b")), extra_options=frozenset(("1", "2")))


@pytest.fixture
async def options_one_in_db(
    fake_options_repository: FakeOptionsRepository,
    fake_uow: FakeUOW,
    options_one: Options,
):
    return await fake_options_repository.add(options=options_one, uow=fake_uow)


@pytest.fixture
def options_one_variant():
    return Options(options=frozenset(("b", "a")), extra_options=frozenset(("1", "2")))


@pytest.fixture
def question_one():
    return Question(user_id="1", question_text="text", question_type=QuestionType.ONE)


@pytest.fixture
def fake_question_rep():
    return FakeQuestionRepository()


@pytest.fixture
async def question_one_in_db(
    question_one: Question, fake_uow: FakeUOW, fake_question_rep: FakeQuestionRepository
):
    return await fake_question_rep.add(question=question_one, uof=fake_uow)
