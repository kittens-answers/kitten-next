from dataclasses import dataclass

from answers.domain.models import QuestionType, TagsType


@dataclass(frozen=True)
class CreateQuestion:
    user_id: str
    question_text: str
    question_type: QuestionType
    options: tuple[str]
    extra_options: tuple[str]
    answer: tuple[tuple[str, str], ...]
    tags: tuple[tuple[TagsType, str], ...]
