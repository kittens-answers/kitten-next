import pytest
from pydantic import ValidationError

from answers.domain import commands


@pytest.fixture
def create_question_command():
    return {
        "question_text": "text",
        "question_type": commands.QuestionType.ONE,
        "options": ["1", "2"],
        "extra_options": [],
    }


class TestCreateQuestion:
    @staticmethod
    @pytest.mark.parametrize(
        "wrong_text",
        ["", 500 * "*"],
        ids=["empty", "too long string"],
    )
    def test_question(create_question_command: dict, wrong_text: str):
        create_question_command["question_text"] = wrong_text
        with pytest.raises(ValidationError):
            commands.CreateQuestion(**create_question_command)

    @staticmethod
    @pytest.mark.parametrize(
        "wrong_options",
        [
            [],
            ["1"],
            ["", "1"],
            ["1", "1", "2"],
            [500 * "*", "2"],
            list(map(str, range(20))),
        ],
        ids=[
            "empty list",
            "only one",
            "empty item",
            "not unique item",
            "too long item",
            "too long list",
        ],
    )
    def test_options(create_question_command: dict, wrong_options: list[str]):
        create_question_command["options"] = wrong_options
        with pytest.raises(ValidationError):
            commands.CreateQuestion(**create_question_command)

    @staticmethod
    @pytest.mark.parametrize(
        "wrong_extra_options",
        [
            [],
            ["1"],
            ["", "1"],
            ["1", "1", "2"],
            [500 * "*", "2"],
            list(map(str, range(20))),
            ["1", "2", "3"],
        ],
        ids=[
            "empty list",
            "only one",
            "empty item",
            "not unique item",
            "too long item",
            "too long list",
            "not equal length with options",
        ],
    )
    def test_extra_options(create_question_command: dict, wrong_extra_options: list[str]):
        create_question_command["extra_options"] = wrong_extra_options
        create_question_command["question_type"] = commands.QuestionType.MATCH
        with pytest.raises(ValidationError):
            commands.CreateQuestion(**create_question_command)

    @staticmethod
    @pytest.mark.parametrize(
        "question_type",
        (v for v in commands.QuestionType if v != commands.QuestionType.MATCH),
    )
    def test_extra_options_with_not_match(create_question_command: dict, question_type: commands.QuestionType):
        create_question_command["question_type"] = question_type
        create_question_command["extra_options"] = list(v + "extra" for v in create_question_command["options"])
        with pytest.raises(ValidationError):
            commands.CreateQuestion(**create_question_command)
