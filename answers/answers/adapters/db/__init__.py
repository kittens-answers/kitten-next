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


async def bootstrap(config: DBSettings | None = None):
    if config is None:
        config = DBSettings()
    engine = get_engine(url=config.url, echo=config.echo)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    await create_tables(engine)
    return async_session
