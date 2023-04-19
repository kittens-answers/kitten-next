from pydantic import BaseModel, Field, validator

from answers.domain.models import QuestionType, TagsType

MAX_LENGTH = 300


class CreateUser(BaseModel):
    user_id: str


class CreateQuestion(BaseModel):
    question_text: str = Field(..., min_length=1, max_length=MAX_LENGTH)
    question_type: QuestionType
    options: list[str] = Field(
        ...,
        min_items=2,
        max_items=10,
        unique_items=True,
        min_length=1,
        max_length=MAX_LENGTH,
    )
    extra_options: list[str] = Field(
        ...,
        min_items=0,
        max_items=10,
        unique_items=True,
        min_length=1,
        max_length=MAX_LENGTH,
    )

    @validator("extra_options")
    def check_extra_answer(cls, v, values):
        question_type = values.get("question_type")
        if question_type == QuestionType.MATCH:
            if len(v) != len(values.get("options")):
                raise ValueError("Length of extra options and options have to be equal")
        else:
            if len(v) > 0:
                raise ValueError("Extra options can be not empty only in match type question")
        return v


class CreateAnswer(BaseModel):
    answer: list[tuple[str, str]]
    is_correct: None | bool = None


class CreateTag(BaseModel):
    tag_name: TagsType
    value: str
