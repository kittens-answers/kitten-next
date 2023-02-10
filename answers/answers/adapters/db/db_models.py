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
    option: Mapped["Option"] = relationship(init=False)
    option_id: Mapped[str] = mapped_column(ForeignKey("option.id"), init=False)
    # answers: Mapped[list["Answer"]] = relationship(init=False)


class Option(Base):
    __tablename__ = "option"

    # question_id: Mapped[str] = mapped_column(ForeignKey("question.id"), unique=True)
    id: Mapped[str] = mapped_column(primary_key=True, default_factory=new_id)
    options: Mapped[list["OptionItem"]] = relationship(init=False)
    extra_options: Mapped[list["ExtraOptionItem"]] = relationship(init=False)


class OptionItem(Base):
    __tablename__ = "option_item"

    option_id: Mapped[str] = mapped_column(
        ForeignKey("option.id"), primary_key=True, init=False
    )
    text: Mapped[str] = mapped_column(
        primary_key=True,
    )


class ExtraOptionItem(Base):
    __tablename__ = "extra_option_item"

    option_id: Mapped[str] = mapped_column(
        ForeignKey("option.id"), primary_key=True, init=False
    )
    text: Mapped[str] = mapped_column(
        primary_key=True,
    )


# class Answer(Base):
#     __tablename__ = "answer"

#     question_id: Mapped[str] = mapped_column(
#         ForeignKey("question.id"), primary_key=True
#     )
#     id: Mapped[str] = mapped_column(primary_key=True, default_factory=new_id)
#     created_by: Mapped[str] = mapped_column(
#         ForeignKey("user.id"), init=False, primary_key=True
#     )


# class AnswerItem(Base):
#     __tablename__ = "answer_item"

#     answer_id: Mapped[str] = mapped_column(ForeignKey("answer.id"), primary_key=True)
#     option: Mapped[str] = mapped_column(primary_key=True)
#     extra_option: Mapped[str] = mapped_column(primary_key=True)


# class Tag(Base):
#     __tablename__ = "tags"

#     answer_id: Mapped[str] = mapped_column(ForeignKey("answer.id"), primary_key=True)
#     name: Mapped[str] = mapped_column(primary_key=True)
#     value: Mapped[str] = mapped_column(primary_key=True)
