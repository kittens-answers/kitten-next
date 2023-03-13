import json
from asyncio import get_event_loop
from contextlib import AbstractContextManager
from dataclasses import asdict
from typing import Any

import typer

from answers.adapters.db import BootStrap
from answers.adapters.repository.sql_alchemy import SQLAlchemyRepository
from answers.domain.aggregate import QuestionWithAnswer
from answers.domain.specifications import TextContains

app = typer.Typer()


@app.command()
def dump():
    with SyncAggregate() as agr:
        users, questions, answers, tags = get_event_loop().run_until_complete(
            agr.dump()
        )
    data = {
        "users": tuple(map(asdict, users)),
        "questions": tuple(map(asdict, questions)),
        "answers": tuple(map(asdict, answers)),
        "tags": tuple(map(asdict, tags)),
    }
    with open("db_dump.json", mode="w") as file:
        json.dump(data, file, ensure_ascii=False, indent=4, cls=FrozenSetEncoder)


@app.command()
def import_dump():
    with open("db_dump.json", mode="r") as file:
        data = json.load(file)

    with SyncAggregate() as agr:
        get_event_loop().run_until_complete(agr.import_from_dict(data))


@app.command()
def search(q: str):
    async def _search(agr: QuestionWithAnswer, q: str):
        async with agr.repository:
            return await agr.repository.questions.list([TextContains(q=q)])

    with SyncAggregate() as agr:
        data = get_event_loop().run_until_complete(_search(agr, q))
        for d in data:
            print(d)


class SyncAggregate(AbstractContextManager):
    def __enter__(self):
        self.boot = BootStrap()
        session = get_event_loop().run_until_complete(self.boot.start())
        rep = SQLAlchemyRepository(session)
        return QuestionWithAnswer(rep)

    def __exit__(self, __exc_type, __exc_value, __traceback):
        get_event_loop().run_until_complete(self.boot.stop())


class FrozenSetEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, frozenset):
            return list(o)
        return super().default(o)


if __name__ == "__main__":
    app()
