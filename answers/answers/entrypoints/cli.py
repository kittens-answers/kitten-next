import json
from asyncio import get_event_loop
from dataclasses import asdict
from typing import Any

import typer

from answers.domain.bootstrap import BootStrap
from answers.domain.specifications import TextContains

app = typer.Typer()


@app.command()
def dump():
    async def _dump():
        async with BootStrap() as boot:
            return await (await boot.get_qwa_aggregate()).dump()

    users, questions, answers, tags = get_event_loop().run_until_complete(_dump())
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
    async def _import_dump(data):
        async with BootStrap() as boot:
            await (await boot.get_qwa_aggregate()).import_from_dict(data)

    with open("db_dump.json", mode="r") as file:
        data = json.load(file)

    get_event_loop().run_until_complete(_import_dump(data=data))


@app.command()
def search(q: str):
    async def _search(q: str):
        async with BootStrap() as boot:
            async with boot.db.get_repository() as repository:
                return await repository.questions.list([TextContains(q=q)])

    data = get_event_loop().run_until_complete(_search(q))
    for d in data:
        print(d)


class FrozenSetEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, frozenset):
            return list(o)
        return super().default(o)


if __name__ == "__main__":
    app()
