from answers.adapters.repository import AbstractRepository
from answers.domain import commands


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
