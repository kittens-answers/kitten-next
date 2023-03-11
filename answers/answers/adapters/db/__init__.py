from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from answers.adapters.db.db_models import Base
from answers.settings import DBSettings


async def create_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


class BootStrap:
    def __init__(self, settings: DBSettings | None = None) -> None:
        self.settings = settings or DBSettings()  # type: ignore
        if self.settings is None:
            raise RuntimeError
        self.url = URL.create(
            drivername=self.settings.sa_settings.drivername,
            username=self.settings.sa_settings.username,
            password=self.settings.sa_settings.password,
            host=self.settings.sa_settings.host,
            port=self.settings.sa_settings.port,
            database=self.settings.sa_settings.database,
        )

    async def start(self):
        self.engine = create_async_engine(self.url, echo=self.settings.sa_settings.echo)
        self.async_session = async_sessionmaker(self.engine, expire_on_commit=False)
        await create_tables(self.engine)
        return self.async_session

    async def stop(self):
        await self.engine.dispose()
