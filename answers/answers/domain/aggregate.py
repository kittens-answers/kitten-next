from rich.progress import track
from sqlalchemy.exc import IntegrityError

from answers.domain import commands, models
from answers.domain.abstract.repository import AbstractRepository


class QuestionWithAnswer:
    def __init__(self, repository: AbstractRepository) -> None:
        self.repository = repository

    async def import_qat(self, dto: commands.ImportQAT):
        async with self.repository:
            user, is_user_created = await self.repository.users.get_or_create(
                dto=commands.CreateUser(user_id=dto.user_id)
            )

            (
                question,
                is_question_created,
            ) = await self.repository.questions.get_or_create(
                dto=commands.CreateQuestion(
                    user_id=user.id,
                    question_text=dto.question_text,
                    question_type=dto.question_type,
                    options=dto.options,
                    extra_options=dto.extra_options,
                )
            )

            answer, is_answer_created = await self.repository.answers.get_or_create(
                dto=commands.CreateAnswer(
                    user_id=user.id, question_id=question.id, answer=dto.answer
                )
            )

            tag, is_tag_created = await self.repository.tags.get_or_create(
                dto=commands.CreateTag(
                    answer_id=answer.id,
                    user_id=user.id,
                    tag_name=commands.TagsType.IS_CORRECT,
                    value=str(dto.is_correct),
                )
            )

            await self.repository.commit()

        return (is_user_created, is_question_created, is_answer_created, is_tag_created)

    async def dump(self):
        async with self.repository:
            users = await self.repository.users.list([])
            questions = await self.repository.questions.list([])
            answers = await self.repository.answers.list([])
            answer_tags = await self.repository.tags.list([])

        return (users, questions, answers, answer_tags)

    async def import_from_dict(self, data: dict):
        users = data.get("users", [])
        inserted_users = 0
        skipped_users = 0
        questions = data.get("questions", [])
        inserted_questions = 0
        skipped_questions = 0
        answers = data.get("answers", [])
        inserted_answers = 0
        skipped_answers = 0
        tags = data.get("tags", [])
        inserted_tags = 0
        skipped_tags = 0

        for user in track(users, description="Users "):
            async with self.repository:
                await self.repository.users.insert(models.User(**user))
                try:
                    await self.repository.commit()
                    inserted_users += 1
                except IntegrityError:
                    skipped_users += 1

        for question in track(questions, description="Questions "):
            async with self.repository:
                await self.repository.questions.insert(models.Question(**question))
                try:
                    await self.repository.commit()
                    inserted_questions += 1
                except IntegrityError:
                    skipped_questions += 1

        for answer in track(answers, description="Answers "):
            async with self.repository:
                await self.repository.answers.insert(models.Answer(**answer))
                try:
                    await self.repository.commit()
                    inserted_answers += 1
                except IntegrityError:
                    skipped_answers += 1

        for tag in track(tags, description="Tags "):
            async with self.repository:
                await self.repository.tags.insert(models.AnswerTag(**tag))
                try:
                    await self.repository.commit()
                    inserted_tags += 1
                except IntegrityError:
                    skipped_tags += 1

        print(f"users inserted: {inserted_users}, skipped {skipped_users}")
        print(f"questions inserted: {inserted_questions}, skipped {skipped_questions}")
        print(f"answers inserted: {inserted_answers}, skipped {skipped_answers}")
        print(f"tags inserted: {inserted_tags}, skipped {skipped_tags}")
