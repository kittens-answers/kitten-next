from answers.adapters.repository import AbstractRepository
from answers.domain import commands


class Importer:
    def __init__(self, repository: AbstractRepository) -> None:
        self.repository = repository

    async def import_qat(self, dto: commands.ImportQAT):
        async with self.repository:
            user = await self.repository.users.get_or_create(
                dto=commands.CreateUser(user_id=dto.user_id)
            )
            question = await self.repository.questions.get_or_create(
                dto=commands.CreateQuestion(
                    user_id=user.id,
                    question_text=dto.question_text,
                    question_type=dto.question_type,
                    options=dto.options,
                    extra_options=dto.extra_options,
                )
            )
            answer = await self.repository.answers.get_or_create(
                dto=commands.CreateAnswer(
                    user_id=user.id, question_id=question.id, answer=dto.answer
                )
            )
            await self.repository.tags.create_or_update(
                dto=commands.CreateTag(
                    answer_id=answer.id,
                    user_id=user.id,
                    tag_name=commands.TagsType.IS_CORRECT,
                    value=str(dto.is_correct),
                )
            )
            await self.repository.commit()

        return answer.id
