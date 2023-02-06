from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncEngine

from answers.adapters.db.db_models import Base
from dataclasses import dataclass


@dataclass
class DBSettings:
    url: str = "sqlite+aiosqlite:///db.db"
    echo: bool = True


async def create_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def get_engine(url: str, echo: bool):
    return create_async_engine(
        url=url,
        echo=echo,
    )


class BootStrap:
    def __init__(self, config: DBSettings | None = None) -> None:
        self.config = config or DBSettings()

    async def start(self):
        self.engine = get_engine(url=self.config.url, echo=self.config.echo)
        self.async_session = async_sessionmaker(self.engine, expire_on_commit=False)
        await create_tables(self.engine)
        return self.async_session

    async def stop(self):
        await self.engine.dispose()
