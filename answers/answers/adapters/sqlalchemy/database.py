from sqlalchemy import URL
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from answers.adapters.sqlalchemy.db_models import Base
from answers.adapters.sqlalchemy.repository import SQLAlchemyRepository
from answers.domain.abstract.database import AbstractDB
from answers.domain.abstract.repository import AbstractRepository
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


class SQLAlchemyDB(AbstractDB):
    def __init__(self, settings: DBSettings | None = None) -> None:
        self.settings = settings or DBSettings()  # type: ignore

    async def start(self):
        self.engine = create_async_engine(
            self.settings.url, echo=self.settings.sqlalchemy_echo
        )
        self.async_session = async_sessionmaker(self.engine, expire_on_commit=False)
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def stop(self):
        await self.engine.dispose()

    def get_repository(self) -> AbstractRepository:
        return SQLAlchemyRepository(self.async_session)
