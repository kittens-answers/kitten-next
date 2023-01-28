from dataclasses import dataclass

from answers.domain import QuestionType


@dataclass(frozen=True)
class Question:
    user_id: str
    question_text: str
    question_type: QuestionType


@dataclass(frozen=True)
class Options:
    options: frozenset[str]
    extra_options: frozenset[str]
