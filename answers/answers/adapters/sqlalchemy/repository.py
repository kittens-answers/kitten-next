from typing import Self

from sqlalchemy import URL, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import selectinload

from answers.adapters.sqlalchemy import db_models
from answers.adapters.sqlalchemy.db_models import Base
from answers.domain import commands, models
from answers.domain.abstract.repository import AbstractRepository, validate_answer
from answers.domain.exceptions import repository_exc
from answers.settings import BaseSettings


class DBSettings(BaseSettings):
    sqlalchemy_drivername: str
    sqlalchemy_username: str | None = None
    sqlalchemy_password: str | None = None
    sqlalchemy_host: str | None = None
    sqlalchemy_port: int | None = None
    sqlalchemy_database: str | None = None
    sqlalchemy_echo: bool = True

    @property
    def url(self):
        return URL.create(
            drivername=self.sqlalchemy_drivername,
            username=self.sqlalchemy_username,
            password=self.sqlalchemy_password,
            host=self.sqlalchemy_host,
            port=self.sqlalchemy_port,
            database=self.sqlalchemy_database,
        )


# async def list(self, specs: list[Specification]) -> Sequence[models.Question]:
#     stmt = select(db_models.Question).options(
#         selectinload(db_models.Question.answers).selectinload(db_models.Answer.tags)
#     )
#     for spec in specs:
#         if isinstance(spec, TextContains):
#             stmt = stmt.where(db_models.Question.text.icontains(spec.q))  # type: ignore
#     questions = (await self.session.scalars(stmt)).all()
#     return tuple(map(models.Question.from_orm, questions))


class SQLAlchemyRepository(AbstractRepository):
    def __init__(self, settings: DBSettings | None = None) -> None:
        self.settings = settings or DBSettings()  # type: ignore
        self.engine = create_async_engine(self.settings.url, echo=self.settings.sqlalchemy_echo)
        self.session_factory = async_sessionmaker(self.engine, expire_on_commit=False)

    async def __aenter__(self) -> Self:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        return self

    async def __aexit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> bool | None:
        await self.engine.dispose()

    async def create_user(self, command: commands.CreateUser) -> models.User:
        async with self.session_factory() as session:
            stmt = select(db_models.User).where(db_models.User.user_id == command.user_id).limit(1)
            user = (await session.scalars(stmt)).first()
            if user is None:
                user = db_models.User(user_id=command.user_id)
                session.add(user)
                await session.commit()
                return models.User.from_orm(user)
            else:
                raise repository_exc.UserAlreadyExist(user=models.User.from_orm(user))

    async def get_user_by_id(self, user_id: str) -> models.User:
        async with self.session_factory() as session:
            stmt = select(db_models.User).where(db_models.User.id == user_id).limit(1)
            user = (await session.scalars(stmt)).first()
            if user is None:
                raise repository_exc.UserDoesNotExist(user_id=user_id)
            return models.User.from_orm(user)

    async def create_question(self, user: models.User, command: commands.CreateQuestion) -> models.Question:
        async with self.session_factory() as session:
            stmt = (
                select(db_models.Question)
                .options(selectinload(db_models.Question.answers).selectinload(db_models.Answer.tags))
                .where(
                    db_models.Question.text == command.question_text,
                    db_models.Question.question_type == command.question_type,
                    db_models.Question.options == db_models.build_option_dict(command.options, command.extra_options),
                )
                .limit(1)
            )
            question = (await session.scalars(stmt)).first()
            if question is None:
                question = db_models.Question(
                    text=command.question_text,
                    question_type=command.question_type,
                    options=db_models.build_option_dict(command.options, command.extra_options),
                    created_by=user.id,
                    answers=[],
                )
                session.add(question)
                await session.commit()
                return models.Question.from_orm(question)
            else:
                raise repository_exc.QuestionAlreadyExist(question=models.Question.from_orm(question))

    async def get_question_by_id(self, question_id: str) -> models.Question:
        async with self.session_factory() as session:
            stmt = (
                select(db_models.Question)
                .options(selectinload(db_models.Question.answers).selectinload(db_models.Answer.tags))
                .where(db_models.Question.id == question_id)
                .limit(1)
            )
            question = (await session.scalars(stmt)).first()
            if question is None:
                raise repository_exc.QuestionDoesNotExist(question_id=question_id)
            return models.Question.from_orm(question)

    async def create_answer(self, user: models.User, question_id: str, command: commands.CreateAnswer) -> models.Answer:
        async with self.session_factory() as session:
            question = await session.get(db_models.Question, question_id)
            if question is None:
                raise repository_exc.QuestionDoesNotExist(question_id=question_id)
            validate_answer(
                options=frozenset(question.options["options"]),
                extra_options=frozenset(question.options["extra_options"]),
                question_type=question.question_type,
                answer=command.answer,
            )
            stmt = (
                select(db_models.Answer)
                .options(selectinload(db_models.Answer.tags))
                .where(
                    db_models.Answer.question_id == question.id,
                    db_models.Answer.answer == db_models.AnswerDict(sorted(command.answer)),
                )
                .limit(1)
            )
        answer = (await session.scalars(stmt)).first()
        if answer is None:
            answer = db_models.Answer(
                question_id=question.id,
                tags=[],
                answer=db_models.AnswerDict(sorted(command.answer)),
                created_by=user.id,
            )
            if command.is_correct is not None:
                answer.tags.append(
                    db_models.Tag(
                        answer_id=answer.id,
                        created_by=user.id,
                        tag_name=db_models.TagsType.IS_CORRECT,
                        value=str(command.is_correct),
                    )
                )
            session.add(answer)
            await session.commit()
            return models.Answer.from_orm(answer)
        else:
            raise repository_exc.AnswerAlreadyExist(answer=models.Answer.from_orm(answer))

    async def get_answer_by_id(self, answer_id: str) -> models.Answer:
        async with self.session_factory() as session:
            stmt = (
                select(db_models.Answer)
                .options(selectinload(db_models.Answer.tags))
                .where(db_models.Answer.id == answer_id)
                .limit(1)
            )
            answer = (await session.scalars(stmt)).first()
            if answer is None:
                raise repository_exc.AnswerDoesNotExist(answer_id=answer_id)
            return models.Answer.from_orm(answer)

    async def add_tag(self, user: models.User, answer_id: str, command: commands.CreateTag) -> models.Tag:
        async with self.session_factory() as session:
            answer = await session.get(db_models.Answer, answer_id)
            if answer is None:
                raise repository_exc.AnswerDoesNotExist(answer_id=answer_id)
            stmt = (
                select(db_models.Tag)
                .where(
                    db_models.Tag.answer_id == answer_id,
                    db_models.Tag.created_by == user.id,
                    db_models.Tag.tag_name == command.tag_name,
                )
                .limit(1)
            )
            tag = (await session.scalars(stmt)).first()
            if tag is None:
                tag = db_models.Tag(
                    answer_id=answer_id, created_by=user.id, tag_name=command.tag_name, value=command.value
                )
                session.add(tag)
                await session.commit()
                return models.Tag.from_orm(tag)
            else:
                if tag.value != command.value:
                    tag.value = command.value
                    session.add(tag)
                    await session.commit()
                    return models.Tag.from_orm(tag)
                else:
                    return models.Tag.from_orm(tag)
