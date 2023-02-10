from dataclasses import dataclass

from answers.domain.models import QuestionType


@dataclass(frozen=True)
class CreateQuestion:
    question_text: str
    question_type: QuestionType
    options: tuple[str] = tuple()
    extra_options: tuple[str] = tuple()
