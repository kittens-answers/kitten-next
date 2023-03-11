from enum import StrEnum

import pytest

from answers.adapters.db import BootStrap
from answers.adapters.repository.sql_alchemy import SQLAlchemyRepository
from answers.settings import DBSettings, SASettings


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
        settlings = DBSettings(sa_settings=SASettings(drivername="sqlite+aiosqlite"))
        bootstrap = BootStrap(settings=settlings)
        session = await bootstrap.start()
        yield SQLAlchemyRepository(session_factory=session)
        await bootstrap.stop()
