import enum
from dataclasses import dataclass


@enum.unique
class QuestionType(enum.StrEnum):
    ONE = "ONE"
    MANY = "MANY"
    ORDER = "ORDER"
    MATCH = "MATCH"


@enum.unique
class AnswerCheckStatus(enum.StrEnum):
    CHECKED = "CHECKED"
    UNCHECKED = "UNCHECKED"


@enum.unique
class TagsType(enum.StrEnum):
    IS_CORRECT = "IS_CORRECT"


@dataclass(frozen=True)
class User:
    user_id: str


@dataclass(frozen=True)
class Question:
    text: str
    question_type: QuestionType
    created_by: str
    id: str | None
    options: frozenset[str]
    extra_options: frozenset[str]


@dataclass(frozen=True)
class Answer:
    answer_id: str
    question_id: str
    answer: tuple[tuple[str, str], ...]
    created_by: str


# @dataclass(frozen=True)
# class Tag:
#     answer_id: str
#     tag_name: TagsType
#     value: str
