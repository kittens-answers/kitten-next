from answers.adapters.db import BootStrap, DBSettings

import pytest

@pytest.fixture
async def sqlite_memory_session_maker():
    config = DBSettings(url="sqlite+aiosqlite://", echo=True)
    bootstrap = BootStrap(config=config)
    session = await bootstrap.start()
    yield session
    await bootstrap.stop()