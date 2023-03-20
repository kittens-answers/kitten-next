from typing import Iterable, Sequence, cast

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from answers.adapters.sqlalchemy import db_models
from answers.domain import commands, models
from answers.domain.abstract.exceptions import DoesExist
from answers.domain.abstract.repository import (
    AbstractAnswerRepository,
    AbstractAnswerTagRepository,
    AbstractQuestionRepository,
    AbstractRepository,
    AbstractUserRepository,
)
from answers.domain.specifications import Specification, TextContains


class SQLAlchemyQuestionRepository(AbstractQuestionRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, dto: commands.CreateQuestion) -> models.Question | None:
        stmt = (
            select(db_models.Question)
            .where(
                db_models.Question.text == dto.question_text,
                db_models.Question.question_type == dto.question_type,
                db_models.Question.options
                == db_models.OptionDict(
                    options=sorted(dto.options), extra_options=sorted(dto.extra_options)
                ),
            )
            .limit(1)
        )
        question = (await self.session.scalars(stmt)).first()
        if question is None:
            return
        else:
            return models.Question.from_orm(question)

    async def create(self, dto: commands.CreateQuestion) -> models.Question:
        question = db_models.Question(
            text=dto.question_text,
            question_type=dto.question_type,
            options=db_models.OptionDict(
                options=sorted(dto.options), extra_options=sorted(dto.extra_options)
            ),
            created_by=dto.user_id,
        )
        self.session.add(question)
        try:
            await self.session.flush()
        except IntegrityError as error:
            raise DoesExist from error
        return models.Question.from_orm(question)

    async def list(self, specs: list[Specification]) -> Sequence[models.Question]:
        stmt = select(db_models.Question)
        for spec in specs:
            if isinstance(spec, TextContains):
                stmt = stmt.where(
                    db_models.Question.text.icontains(spec.q)  # type: ignore
                )
        questions = (await self.session.scalars(stmt)).all()
        return tuple(map(models.Question.from_orm, questions))

    async def insert(self, model: models.Question):
        try:
            self.session.add(
                db_models.Question(
                    text=model.text,
                    question_type=model.question_type,
                    options=db_models.OptionDict(
                        options=sorted(model.options.keys()),
                        extra_options=sorted(
                            cast(Iterable[str], model.options.values())
                        ),
                    ),
                    created_by=model.created_by,
                    id=model.id,
                )
            )
            await self.session.flush()
        except IntegrityError as error:
            raise DoesExist from error


class SQLAlchemyUserRepository(AbstractUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, dto: commands.CreateUser) -> models.User | None:
        user = await self.session.get(db_models.User, dto.user_id)
        if user is None:
            return
        else:
            return models.User.from_orm(user)

    async def create(self, dto: commands.CreateUser) -> models.User:
        user = db_models.User(id=dto.user_id)
        self.session.add(user)
        await self.session.flush()
        return models.User.from_orm(user)

    async def list(self, specs: list[Specification]) -> Sequence[models.User]:
        stmt = select(db_models.User)
        users = (await self.session.scalars(stmt)).all()
        return tuple(map(models.User.from_orm, users))

    async def insert(self, model: models.User):
        try:
            self.session.add(db_models.User(id=model.id))
            await self.session.flush()
        except IntegrityError as error:
            raise DoesExist from error


class SQLAlchemyAnswerRepository(AbstractAnswerRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, dto: commands.CreateAnswer) -> models.Answer | None:
        stmt = (
            select(db_models.Answer)
            .where(
                db_models.Answer.question_id == dto.question_id,
                db_models.Answer.answer == db_models.AnswerDict(sorted(dto.answer)),
            )
            .limit(1)
        )
        answer = (await self.session.scalars(stmt)).first()
        if answer is None:
            return None
        else:
            return models.Answer.from_orm(answer)

    async def create(self, dto: commands.CreateAnswer) -> models.Answer:
        answer = db_models.Answer(
            question_id=dto.question_id,
            answer=db_models.AnswerDict(sorted(dto.answer)),
            created_by=dto.user_id,
        )
        answer.created_by = dto.user_id
        self.session.add(answer)
        await self.session.flush()
        return models.Answer.from_orm(answer)

    async def list(self, specs: list[Specification]) -> Sequence[models.Answer]:
        stmt = select(db_models.Answer)
        answers = (await self.session.scalars(stmt)).all()
        return tuple(map(models.Answer.from_orm, answers))

    async def insert(self, model: models.Answer):
        try:
            self.session.add(
                db_models.Answer(
                    question_id=model.question_id,
                    answer=model.answer,
                    created_by=model.created_by,
                    id=model.id,
                )
            )
            await self.session.flush()
        except IntegrityError as error:
            raise DoesExist from error


class SQLAlchemyAnswerTagRepository(AbstractAnswerTagRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, dto: commands.CreateTag) -> models.AnswerTag | None:
        stmt = (
            select(db_models.AnswerTag)
            .where(
                db_models.AnswerTag.answer_id == dto.answer_id,
                db_models.AnswerTag.created_by == dto.user_id,
                db_models.AnswerTag.tag_name == dto.tag_name,
            )
            .limit(1)
        )
        tag = (await self.session.scalars(stmt)).first()
        if tag is not None:
            return models.AnswerTag.from_orm(tag)

    async def create(self, dto: commands.CreateTag) -> models.AnswerTag:
        tag = db_models.AnswerTag(
            answer_id=dto.answer_id,
            tag_name=dto.tag_name,
            value=dto.value,
            created_by=dto.user_id,
        )
        self.session.add(tag)
        await self.session.flush()
        return models.AnswerTag.from_orm(tag)

    async def list(self, specs: list[Specification]) -> Sequence[models.AnswerTag]:
        stmt = select(db_models.AnswerTag)
        answer_tags = (await self.session.scalars(stmt)).all()
        return tuple(map(models.AnswerTag.from_orm, answer_tags))

    async def insert(self, model: models.AnswerTag):
        try:
            self.session.add(
                db_models.AnswerTag(
                    answer_id=model.answer_id,
                    created_by=model.created_by,
                    tag_name=model.tag_name,
                    value=model.value,
                    id=model.id,
                )
            )
            await self.session.flush()
        except IntegrityError as error:
            raise DoesExist from error


class SQLAlchemyRepository(AbstractRepository):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session = session_factory()
        self.users = SQLAlchemyUserRepository(session=self._session)
        self.questions = SQLAlchemyQuestionRepository(session=self._session)
        self.answers = SQLAlchemyAnswerRepository(session=self._session)
        self.tags = SQLAlchemyAnswerTagRepository(session=self._session)

    async def __aenter__(self):
        self._session.begin()
        return self

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()
