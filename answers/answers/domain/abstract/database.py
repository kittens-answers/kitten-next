import abc

from answers.domain.abstract.repository import AbstractRepository


class AbstractDB(abc.ABC):  # pragma: no cover
    @abc.abstractmethod
    async def start(self):
        ...

    @abc.abstractmethod
    async def stop(self):
        ...

    @abc.abstractmethod
    def get_repository(self) -> AbstractRepository:
        ...
