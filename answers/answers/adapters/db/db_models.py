from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
    relationship,
)

from answers.adapters.db.utils import new_id


class Base(MappedAsDataclass, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[str] = mapped_column(primary_key=True)


class Question(Base):
    __tablename__ = "question"
    __table_args__ = (UniqueConstraint("text", "question_type", name="question_uc"),)

    text: Mapped[str] = mapped_column()
    question_type: Mapped[str] = mapped_column()
    id: Mapped[str] = mapped_column(primary_key=True, default_factory=new_id)
    created_by: Mapped[str] = mapped_column(ForeignKey("user.id"), init=False)
    user: Mapped[User] = relationship(init=False)
    options: Mapped[list["Option"]] = relationship(init=False)
    extra_options: Mapped[list["ExtraOption"]] = relationship(init=False)
    answers: Mapped[list["Answer"]] = relationship(init=False)


class Option(Base):
    __tablename__ = "option"

    question_id: Mapped[str] = mapped_column(
        ForeignKey("question.id"), primary_key=True
    )
    text: Mapped[str] = mapped_column(
        primary_key=True,
    )


class ExtraOption(Base):
    __tablename__ = "extra_option"

    question_id: Mapped[str] = mapped_column(
        ForeignKey("question.id"), primary_key=True
    )
    text: Mapped[str] = mapped_column(
        primary_key=True,
    )


class Answer(Base):
    __tablename__ = "answer"

    question_id: Mapped[str] = mapped_column(
        ForeignKey("question.id"), primary_key=True
    )
    id: Mapped[str] = mapped_column(primary_key=True, default_factory=new_id)
    created_by: Mapped[str] = mapped_column(
        ForeignKey("user.id"), init=False, primary_key=True
    )


class AnswerItem(Base):
    __tablename__ = "answer_item"

    answer_id: Mapped[str] = mapped_column(ForeignKey("answer.id"), primary_key=True)
    option: Mapped[str] = mapped_column(primary_key=True)
    extra_option: Mapped[str] = mapped_column(primary_key=True)


class Tag(Base):
    __tablename__ = "tags"

    answer_id: Mapped[str] = mapped_column(ForeignKey("answer.id"), primary_key=True)
    name: Mapped[str] = mapped_column(primary_key=True)
    value: Mapped[str] = mapped_column(primary_key=True)