from answers.adapters.repository import AbstractQuestionRepository
from answers.domain import models
from answers.domain.commands import CreateQuestion
from answers.service_layer.unit_of_work import AbstractUOWFabric


class Question:
    def __init__(
        self, repo: AbstractQuestionRepository, uow_maker: AbstractUOWFabric
    ) -> None:
        self.repo = repo
        self.uow_maker = uow_maker

    async def get_or_create(self, dto: CreateQuestion, user_id: str) -> models.Question:
        async with self.uow_maker as uow:
            question = await self.repo.get(dto=dto, uow=uow)
            if question is None:
                question = await self.repo.create(dto=dto, user_id=user_id, uow=uow)
            await uow.commit()
            return question
