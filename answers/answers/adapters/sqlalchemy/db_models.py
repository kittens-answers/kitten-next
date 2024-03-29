from typing import TypedDict

from sqlalchemy import JSON, ForeignKey, UniqueConstraint
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
    relationship,
)

from answers.domain.models import AnswerDict, QuestionType, TagsType
from answers.domain.utils import new_id


class OptionDict(TypedDict):
    options: list[str]
    extra_options: list[str]


def build_option_dict(options: list[str], extra_options: list[str]) -> OptionDict:
    return OptionDict(options=sorted(options), extra_options=sorted(extra_options))


class Base(DeclarativeBase, MappedAsDataclass):
    pass


class User(Base):
    __tablename__ = "user"

    user_id: Mapped[str] = mapped_column(unique=True)
    id: Mapped[str] = mapped_column(primary_key=True, default_factory=new_id)


class Question(Base):
    __tablename__ = "question"
    __table_args__ = (UniqueConstraint("text", "question_type", "options"),)

    text: Mapped[str] = mapped_column()
    answers: Mapped[list["Answer"]] = relationship()
    question_type: Mapped[QuestionType] = mapped_column()
    options: Mapped[OptionDict] = mapped_column(JSON)
    created_by: Mapped[str] = mapped_column(ForeignKey("user.id"))
    id: Mapped[str] = mapped_column(primary_key=True, default_factory=new_id)


class Answer(Base):
    __tablename__ = "answer"
    __table_args__ = (UniqueConstraint("question_id", "answer"),)

    question_id: Mapped[str] = mapped_column(ForeignKey("question.id"))
    tags: Mapped[list["Tag"]] = relationship()
    answer: Mapped[AnswerDict] = mapped_column(JSON)
    created_by: Mapped[str] = mapped_column(ForeignKey("user.id"))
    id: Mapped[str] = mapped_column(primary_key=True, default_factory=new_id)


class Tag(Base):
    __tablename__ = "answer_tag"
    __table_args__ = (UniqueConstraint("answer_id", "created_by", "tag_name"),)

    answer_id: Mapped[str] = mapped_column(ForeignKey("answer.id"))
    created_by: Mapped[str] = mapped_column(ForeignKey("user.id"))
    tag_name: Mapped[TagsType] = mapped_column()
    value: Mapped[str] = mapped_column()
    id: Mapped[str] = mapped_column(primary_key=True, default_factory=new_id)
