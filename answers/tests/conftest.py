from enum import StrEnum

import pytest

from answers.adapters.sqlalchemy.database import DBSettings, SQLAlchemyDB


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
        settlings = DBSettings(
            sqlalchemy_drivername="sqlite+aiosqlite", sqlalchemy_database=None
        )
        db = SQLAlchemyDB(settings=settlings)
        await db.start()
        yield db.get_repository()
        await db.stop()
