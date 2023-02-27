import pytest

from answers.domain.commands import CreateQuestion, QuestionType


@pytest.mark.parametrize(
    "test_input",
    [
        CreateQuestion(
            question_text="?",
            question_type=QuestionType.ONE,
            options=[],
            extra_options=[],
        ),
        CreateQuestion(
            question_text="?",
            question_type=QuestionType.ONE,
            options=["1", "2"],
            extra_options=[],
        ),
        CreateQuestion(
            question_text="?",
            question_type=QuestionType.ORDER,
            options=["1", "2"],
            extra_options=[],
        ),
        CreateQuestion(
            question_text="?",
            question_type=QuestionType.MATCH,
            options=["1", "2"],
            extra_options=["a", "b"],
        ),
    ],
)
def test_correct(test_input: CreateQuestion):
    test_input.validate()


@pytest.mark.parametrize(
    "test_input",
    [
        CreateQuestion(
            question_text="",
            question_type=QuestionType.ONE,
            options=[],
            extra_options=[],
        ),
        CreateQuestion(
            question_text="?",
            question_type=QuestionType.ONE,
            options=["1", "2"],
            extra_options=["a", "b"],
        ),
        CreateQuestion(
            question_text="?",
            question_type=QuestionType.ONE,
            options=["1"],
            extra_options=[],
        ),
        CreateQuestion(
            question_text="?",
            question_type=QuestionType.ORDER,
            options=["1", "2"],
            extra_options=["a", "b"],
        ),
        CreateQuestion(
            question_text="?",
            question_type=QuestionType.ORDER,
            options=["1"],
            extra_options=[],
        ),
        CreateQuestion(
            question_text="?",
            question_type=QuestionType.ORDER,
            options=[],
            extra_options=[],
        ),
        CreateQuestion(
            question_text="?",
            question_type=QuestionType.MATCH,
            options=["1"],
            extra_options=["a"],
        ),
        CreateQuestion(
            question_text="?",
            question_type=QuestionType.MATCH,
            options=["1", "2"],
            extra_options=["a", "b", "c"],
        ),
        CreateQuestion(
            question_text="?",
            question_type=QuestionType.MATCH,
            options=[],
            extra_options=[],
        ),
        CreateQuestion(
            question_text="?",
            question_type=QuestionType.MATCH,
            options=["1", ""],
            extra_options=["a", "b"],
        ),
        CreateQuestion(
            question_text="?",
            question_type=QuestionType.MATCH,
            options=["1", "2"],
            extra_options=["a", ""],
        ),
    ],
)
def test_incorrect(test_input: CreateQuestion):
    with pytest.raises(ValueError):
        test_input.validate()
