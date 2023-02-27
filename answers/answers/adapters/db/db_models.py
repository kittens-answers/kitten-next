from typing import TypedDict

from sqlalchemy import JSON, ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column

from answers.adapters.db.utils import new_id
from answers.domain.models import QuestionType


class OptionDict(TypedDict):
    options: list[str]
    extra_options: list[str]


AnswerDict = dict[str, str]


class Base(DeclarativeBase, MappedAsDataclass):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[str] = mapped_column(primary_key=True)


class Question(Base):
    __tablename__ = "question"
    __table_args__ = (UniqueConstraint("text", "question_type", "options"),)

    text: Mapped[str] = mapped_column()
    question_type: Mapped[QuestionType] = mapped_column()
    options: Mapped[OptionDict] = mapped_column(JSON)
    id: Mapped[str] = mapped_column(primary_key=True, default_factory=new_id)
    created_by: Mapped[str] = mapped_column(ForeignKey("user.id"), init=False)
    # answers: Mapped[list["Answer"]] = relationship(init=False)


class Answer(Base):
    __tablename__ = "answer"

    question_id: Mapped[str] = mapped_column(ForeignKey("question.id"))
    answer: Mapped[AnswerDict] = mapped_column(JSON, unique=True)
    id: Mapped[str] = mapped_column(primary_key=True, default_factory=new_id)
    created_by: Mapped[str] = mapped_column(ForeignKey("user.id"), init=False)
