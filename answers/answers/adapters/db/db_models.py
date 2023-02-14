from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
    relationship,
)

from answers.adapters.db.utils import new_id
from answers.domain.models import QuestionType


class Base(MappedAsDataclass, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[str] = mapped_column(primary_key=True)


class Question(Base):
    __tablename__ = "question"

    text: Mapped[str] = mapped_column()
    question_type: Mapped[QuestionType] = mapped_column()
    id: Mapped[str] = mapped_column(primary_key=True, default_factory=new_id)
    created_by: Mapped[str] = mapped_column(ForeignKey("user.id"), init=False)
    options: Mapped[list["OptionItem"]] = relationship(init=False)
    extra_options: Mapped[list["ExtraOptionItem"]] = relationship(init=False)
    # answers: Mapped[list["Answer"]] = relationship(init=False)


class OptionItem(Base):
    __tablename__ = "option_item"

    question_id: Mapped[str] = mapped_column(
        ForeignKey("question.id"), primary_key=True, init=False
    )
    text: Mapped[str] = mapped_column(primary_key=True)


class ExtraOptionItem(Base):
    __tablename__ = "extra_option_item"

    question_id: Mapped[str] = mapped_column(
        ForeignKey("question.id"), primary_key=True, init=False
    )
    text: Mapped[str] = mapped_column(primary_key=True)


class Answer(Base):
    __tablename__ = "answer"

    question_id: Mapped[str] = mapped_column(ForeignKey("question.id"))
    id: Mapped[str] = mapped_column(primary_key=True, default_factory=new_id)
    created_by: Mapped[str] = mapped_column(ForeignKey("user.id"), init=False)
    answer: Mapped[list["AnswerItem"]] = relationship(init=False)
    # extra_options: Mapped[list["ExtraAnswerItem"]] = relationship(init=False)


class AnswerItem(Base):
    __tablename__ = "answer_item"

    answer_id: Mapped[str] = mapped_column(
        ForeignKey("answer.id"), primary_key=True, init=False
    )
    left: Mapped[str] = mapped_column(primary_key=True)
    right: Mapped[str] = mapped_column(primary_key=True)


# class ExtraAnswerItem(Base):
#     __tablename__ = "extra_answer_item"

#     answer_id: Mapped[str] = mapped_column(ForeignKey("answer.id"), primary_key=True)
#     text: Mapped[str] = mapped_column(primary_key=True)


# class Tag(Base):
#     __tablename__ = "tags"

#     answer_id: Mapped[str] = mapped_column(ForeignKey("answer.id"), primary_key=True)
#     name: Mapped[str] = mapped_column(primary_key=True)
#     value: Mapped[str] = mapped_column(primary_key=True)
