from asyncio import get_event_loop
from pathlib import Path

import typer
from rich.progress import track

from answers.adapters.json_file.database import JsonFileDB, JsonFileDBSettings
from answers.domain.abstract.exceptions import DoesExist
from answers.domain.bootstrap import BootStrap

app = typer.Typer()


@app.command()
def dump(file_path: Path):
    async def _dump():
        async with BootStrap() as boot:
            default_repository = (await boot.get_qwa_aggregate()).repository
            async with default_repository:
                users = await default_repository.users.list([])
                questions = await default_repository.questions.list([])
                answers = await default_repository.answers.list([])
                answer_tags = await default_repository.tags.list([])

        json_file_repository = JsonFileDB(
            JsonFileDBSettings(file_path=file_path)
        ).get_repository()
        json_file_repository.data.users = list(users)
        json_file_repository.data.questions = list(questions)
        json_file_repository.data.answers = list(answers)
        json_file_repository.data.tags = list(answer_tags)

        await json_file_repository.commit()

    get_event_loop().run_until_complete(_dump())


@app.command()
def import_dump(file_path: Path):
    async def _import_dump():
        json_file_repository = JsonFileDB(
            JsonFileDBSettings(file_path=file_path)
        ).get_repository()
        async with BootStrap() as boot:
            default_repository = (await boot.get_qwa_aggregate()).repository

            users_added = 0
            users_skipped = 0
            for user in track(
                json_file_repository.data.users, description="Users".ljust(10)
            ):
                try:
                    async with default_repository:
                        await default_repository.users.insert(user)
                        await default_repository.commit()
                        users_added += 1
                except DoesExist:
                    users_skipped += 1

            questions_added = 0
            questions_skipped = 0
            for question in track(
                json_file_repository.data.questions, description="Questions".ljust(10)
            ):
                try:
                    async with default_repository:
                        await default_repository.questions.insert(question)
                        await default_repository.commit()
                        questions_added += 1
                except DoesExist:
                    questions_skipped += 1

            answers_added = 0
            answers_skipped = 0
            for answer in track(
                json_file_repository.data.answers, description="Answers".ljust(10)
            ):
                try:
                    async with default_repository:
                        await default_repository.answers.insert(answer)
                        await default_repository.commit()
                        answers_added += 1
                except DoesExist:
                    answers_skipped += 1

            tags_added = 0
            tags_skipped = 0
            for tag in track(
                json_file_repository.data.tags, description="Tags".ljust(10)
            ):
                try:
                    async with default_repository:
                        await default_repository.tags.insert(tag)
                        await default_repository.commit()
                        tags_added += 1
                except DoesExist:
                    tags_skipped += 1

        print(f"user added: {users_added}, sipped {users_skipped}")
        print(f"question added: {questions_added}, sipped {questions_skipped}")
        print(f"answer added: {answers_added}, sipped {answers_skipped}")
        print(f"tag added: {tags_added}, sipped {tags_skipped}")

    get_event_loop().run_until_complete(_import_dump())


if __name__ == "__main__":
    app()
