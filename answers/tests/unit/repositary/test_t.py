import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

pytestmark = pytest.mark.anyio


async def test_t(sqlite_memory_session_maker: async_sessionmaker[AsyncSession]):
    async with sqlite_memory_session_maker():
        assert True
