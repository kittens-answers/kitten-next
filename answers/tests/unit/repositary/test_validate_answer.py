import pytest

from answers.domain.abstract.repository import validate_answer
from answers.domain.exceptions.repository_exc import AnswerCanNotBeAddedToQuestion
from answers.domain.models import QuestionType


@pytest.mark.parametrize(
    ["options", "extra_options", "question_type", "answer", "raises"],
    [
        [
            frozenset(),
            frozenset(),
            QuestionType.ONE,
            [("1", "True"), ("2", "False")],
            False,
        ],
        [
            frozenset(("1", "2")),
            frozenset(),
            QuestionType.ONE,
            [("1", "True"), ("2", "False")],
            False,
        ],
        [
            frozenset(),
            frozenset(),
            QuestionType.ONE,
            [("1", "True"), ("2", "False"), ("3", True)],
            True,
        ],
        [
            frozenset(),
            frozenset(),
            QuestionType.ONE,
            [("1", "True"), ("2", "No")],
            True,
        ],
        [
            frozenset(("1", "3")),
            frozenset(),
            QuestionType.ONE,
            [("1", "True"), ("2", "False")],
            True,
        ],
        [
            frozenset(),
            frozenset(),
            QuestionType.ONE,
            [("1", "False"), ("2", "False")],
            True,
        ],
        [
            frozenset(),
            frozenset(),
            QuestionType.MANY,
            [("1", "True"), ("2", "True")],
            False,
        ],
        [
            frozenset(),
            frozenset(),
            QuestionType.ORDER,
            [("a", "1"), ("b", "2")],
            False,
        ],
        [
            frozenset(),
            frozenset(),
            QuestionType.ORDER,
            [("a", "1"), ("b", "3")],
            True,
        ],
        [
            frozenset(),
            frozenset(),
            QuestionType.MATCH,
            [("1", "a"), ("2", "b")],
            False,
        ],
        [
            frozenset(("1", "2")),
            frozenset(("a", "b")),
            QuestionType.MATCH,
            [("1", "a"), ("2", "b")],
            False,
        ],
        [
            frozenset(("1", "2")),
            frozenset(("a", "c")),
            QuestionType.MATCH,
            [("1", "a"), ("2", "b")],
            True,
        ],
        [
            frozenset(("1", "2")),
            frozenset(("a", "b", "c")),
            QuestionType.MATCH,
            [("1", "a"), ("2", "b")],
            True,
        ],
    ],
)
def test_validate_answer(
    options: frozenset[str],
    extra_options: frozenset[str],
    question_type: QuestionType,
    answer: list[tuple[str, str]],
    raises: bool,
):
    if raises:
        with pytest.raises(AnswerCanNotBeAddedToQuestion):
            validate_answer(
                options=options,
                extra_options=extra_options,
                question_type=question_type,
                answer=answer,
            )
    else:
        assert validate_answer(
            options=options,
            extra_options=extra_options,
            question_type=question_type,
            answer=answer,
        )
