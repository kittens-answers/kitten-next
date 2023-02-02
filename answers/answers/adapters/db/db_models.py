from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column


class Base(MappedAsDataclass, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[str] = mapped_column(primary_key=True)


class Question(Base):
    __tablename__ = "question"
    __table_args__ = (UniqueConstraint("text", "question_type", name="question_uc"),)

    id: Mapped[str] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column()
    question_type: Mapped[str] = mapped_column()
