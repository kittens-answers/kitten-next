import pytest

from answers.domain.abstract.repository import AbstractRepository
from answers.domain.aggregate import QuestionWithAnswer
from answers.domain.commands import ImportQAT, QuestionType

pytestmark = pytest.mark.anyio


@pytest.fixture
def importer(repository: AbstractRepository):
    return QuestionWithAnswer(repository=repository)


async def test_import(importer: QuestionWithAnswer):
    res = await importer.import_qat(
        dto=ImportQAT(
            user_id="user",
            question_text="how?",
            question_type=QuestionType.ONE,
            options=["1", "2", "3"],
            extra_options=[],
            answer=[("1", str(True)), ("2", str(False)), ("3", str(False))],
            is_correct=True,
        )
    )

    assert res == (True, True, True, True)
