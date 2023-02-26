import abc
from types import TracebackType
from answers.adapters.repository import AbstractQuestionRepository
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


class AbstractUOW(abc.ABC):
    questions: AbstractQuestionRepository

    async def __aenter__(self):
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ):
        await self.rollback()

    @abc.abstractmethod
    async def commit(self):
        ...

    @abc.abstractmethod
    async def rollback(self):
        ...


class SQLAlchemyUOW(AbstractUOW):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self.session = session_factory()

    async def __aenter__(self):
        self.session.begin()
        return self

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
