from dataclasses import dataclass

from answers.domain.models import QuestionType


@dataclass()
class CreateQuestion:
    question_text: str
    question_type: QuestionType
    options: list[str]
    extra_options: list[str]


@dataclass()
class CreateAnswer:
    question_id: str
    answer: list[tuple[str, str]]
