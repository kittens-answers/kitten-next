import enum
from dataclasses import dataclass


@enum.unique
class QuestionType(enum.StrEnum):
    ONE = "ONE"
    MANY = "MANY"
    ORDER = "ORDER"
    MATCH = "MATCH"


@enum.unique
class TagsType(enum.StrEnum):
    IS_CORRECT = "IS_CORRECT"


@dataclass(frozen=True)
class User:
    id: str


@dataclass(frozen=True)
class Question:
    text: str
    question_type: QuestionType
    created_by: str
    id: str
    options: frozenset[str]
    extra_options: frozenset[str]


@dataclass(frozen=True)
class Answer:
    id: str
    question_id: str
    answer: tuple[tuple[str, str], ...]
    created_by: str


@dataclass(frozen=True)
class AnswerTag:
    id: str
    answer_id: str
    user_id: str
    tag_name: TagsType
    value: str
