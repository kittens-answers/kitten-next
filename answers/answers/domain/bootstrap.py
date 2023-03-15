from contextlib import AbstractAsyncContextManager
from typing import Type

from answers.adapters.sqlalchemy.database import SQLAlchemyDB
from answers.domain.abstract.database import AbstractDB
from answers.domain.aggregate import QuestionWithAnswer
from answers.settings import BootStrapSettings, DBTypeEnum


class BootStrap(AbstractAsyncContextManager):
    def __init__(self, db_type: Type[AbstractDB] | None = None) -> None:
        if db_type:
            self.db = db_type()
        else:
            settings = BootStrapSettings()  # type: ignore
            match settings.db_type:
                case DBTypeEnum.SQLALCHEMY:
                    self.db = SQLAlchemyDB()

    async def __aenter__(self):
        await self.db.start()
        return self

    async def __aexit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> bool | None:
        await self.db.stop()

    async def get_qwa_aggregate(self) -> QuestionWithAnswer:
        return QuestionWithAnswer(self.db.get_repository())
