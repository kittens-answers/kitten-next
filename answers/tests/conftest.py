from enum import StrEnum

import pytest

from answers.adapters.db import BootStrap, DBSettings
from answers.adapters.repository.sql_alchemy import SQLAlchemyRepository


@pytest.fixture
def anyio_backend():
    return "asyncio"


class TestReps(StrEnum):
    IN_MEMORY_SQLITE = "IN_MEMORY_SQLITE"


@pytest.fixture(
    params=[
        TestReps.IN_MEMORY_SQLITE,
    ]
)
async def repository(request):
    if request.param == TestReps.IN_MEMORY_SQLITE:
        config = DBSettings(url="sqlite+aiosqlite://", echo=False)
        bootstrap = BootStrap(config=config)
        session = await bootstrap.start()
        yield SQLAlchemyRepository(session_factory=session)
        await bootstrap.stop()
