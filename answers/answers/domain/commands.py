from dataclasses import dataclass

from answers.domain.models import QuestionType, TagsType


@dataclass()
class CreateUser:
    user_id: str


@dataclass()
class CreateQuestion:
    user_id: str
    question_text: str
    question_type: QuestionType
    options: list[str]
    extra_options: list[str]


@dataclass()
class CreateAnswer:
    user_id: str
    question_id: str
    answer: list[tuple[str, str]]


@dataclass()
class CreateTag:
    answer_id: str
    user_id: str
    tag_name: TagsType
    value: str


@dataclass()
class ImportQAT:
    user_id: str
    question_text: str
    question_type: QuestionType
    options: list[str]
    extra_options: list[str]
    answer: list[tuple[str, str]]
    is_correct: bool
