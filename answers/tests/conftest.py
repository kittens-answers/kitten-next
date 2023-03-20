from enum import StrEnum
from pathlib import Path

import pytest

from answers.adapters.json_file.database import JsonFileDB, JsonFileDBSettings
from answers.adapters.sqlalchemy.database import DBSettings, SQLAlchemyDB


@pytest.fixture
def anyio_backend():
    return "asyncio"


class TestReps(StrEnum):
    IN_MEMORY_SQLITE = "IN_MEMORY_SQLITE"
    JSON_FILE = "JSON_FILE"


@pytest.fixture(
    params=[
        TestReps.IN_MEMORY_SQLITE,
        TestReps.JSON_FILE,
    ]
)
async def repository(request, tmp_path: Path):
    if request.param == TestReps.IN_MEMORY_SQLITE:
        settlings = DBSettings(
            sqlalchemy_drivername="sqlite+aiosqlite", sqlalchemy_database=None
        )
        db = SQLAlchemyDB(settings=settlings)
        await db.start()
        yield db.get_repository()
        await db.stop()
    elif request.param == TestReps.JSON_FILE:
        settlings = JsonFileDBSettings(file_path=tmp_path / "dump.json")
        db = JsonFileDB(settings=settlings)
        await db.start()
        yield db.get_repository()
        await db.stop()
