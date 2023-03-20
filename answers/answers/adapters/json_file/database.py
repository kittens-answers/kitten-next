from pathlib import Path

from answers.adapters.json_file.repository import JSONFileRepository
from answers.domain.abstract.database import AbstractDB
from answers.settings import BaseSettings


class JsonFileDBSettings(BaseSettings):
    file_path: Path


class JsonFileDB(AbstractDB):
    def __init__(self, settings: JsonFileDBSettings | None = None) -> None:
        self.settings = settings or JsonFileDBSettings()  # type: ignore

    async def start(self):
        ...

    async def stop(self):
        ...

    def get_repository(self) -> JSONFileRepository:
        return JSONFileRepository(self.settings.file_path)
