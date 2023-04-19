import enum
from typing import TypedDict

from pydantic import BaseModel, Field, SecretStr


class OptionDict(TypedDict):
    options: frozenset[str]
    extra_options: frozenset[str]


AnswerDict = dict[str, str]


@enum.unique
class QuestionType(enum.StrEnum):
    ONE = "ONE"
    MANY = "MANY"
    ORDER = "ORDER"
    MATCH = "MATCH"


@enum.unique
class TagsType(enum.StrEnum):
    IS_CORRECT = "IS_CORRECT"
    TEST = "TEST"


class User(BaseModel):
    class Config:
        orm_mode = True

    id: str
    user_id: SecretStr


class Tag(BaseModel):
    class Config:
        orm_mode = True

    id: str
    answer_id: str
    created_by: str
    tag_name: TagsType
    value: str


class Answer(BaseModel):
    class Config:
        orm_mode = True

    id: str
    question_id: str
    answer: AnswerDict
    created_by: str
    tags: list[Tag] = Field(default_factory=list)


class Question(BaseModel):
    class Config:
        json_encoders = {frozenset: lambda v: sorted(v)}
        orm_mode = True

    text: str
    question_type: QuestionType
    created_by: str
    id: str
    options: OptionDict
    answers: list[Answer] = Field(default_factory=list)
