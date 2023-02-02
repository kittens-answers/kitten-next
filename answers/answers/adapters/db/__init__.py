import asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from answers.adapters.db.db_models import Base

engine = create_async_engine(
    "sqlite+aiosqlite:///db.db",
    echo=True,
)

async_session = async_sessionmaker(engine, expire_on_commit=False)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def main():
    await create_tables()
    async with async_session() as session:
        await session.commit()


asyncio.run(main())
