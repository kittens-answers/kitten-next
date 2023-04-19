import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient

from answers.domain import commands, models
from answers.domain.abstract.repository import AbstractRepository
from answers.entrypoints.api.routers import RoutsNames

pytestmark = pytest.mark.anyio


class Base:
    _app: FastAPI
    client: AsyncClient
    _route_name: RoutsNames

    @pytest.fixture(autouse=True)
    def _inject(self, app: FastAPI, client: AsyncClient, repository: AbstractRepository):
        self.client = client
        self._app = app
        self.repository = repository

    def get_url(self, **kwargs):
        return self._app.url_path_for(self._route_name, **kwargs)


class TestCreateUser(Base):
    _route_name = RoutsNames.CREATE_USER

    async def test_create(self, create_user_command: commands.CreateUser):
        response = await self.client.post(self.get_url(), json=create_user_command.dict())
        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.usefixtures("user_in_db")
    async def test_raise(self, create_user_command: commands.CreateUser):
        response = await self.client.post(self.get_url(), json=create_user_command.dict())
        assert response.status_code == status.HTTP_409_CONFLICT


class TestGetUser(Base):
    _route_name = RoutsNames.GET_USER

    async def test_get(self):
        response = await self.client.get(self.get_url(user_id="wrong"))
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "error" in response.json()


class TestCreateQuestion(Base):
    _route_name = RoutsNames.CREATE_QUESTION

    async def test_create(self, create_question_command: commands.CreateQuestion, user_in_db: models.User):
        response = await self.client.post(
            self.get_url(), params={"user_id": user_in_db.id}, json=create_question_command.dict()
        )
        assert response.status_code == status.HTTP_201_CREATED
        question = models.Question.parse_obj(response.json())
        assert question == (await self.repository.get_question_by_id(question.id))

    @pytest.mark.usefixtures("question_in_db")
    async def test_raise(self, create_question_command: commands.CreateQuestion, user_in_db: models.User):
        response = await self.client.post(
            self.get_url(), params={"user_id": user_in_db.id}, json=create_question_command.dict()
        )
        assert response.status_code == status.HTTP_409_CONFLICT
        assert "error" in response.json()


class TestGetQuestion(Base):
    _route_name = RoutsNames.GET_QUESTION

    async def test_get_question_by_id_if_not_exist(self):
        response = await self.client.get(self.get_url(question_id="wrong"))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_get_question_by_id_if_exist(self, question_in_db: models.Question):
        response = await self.client.get(self.get_url(question_id=question_in_db.id))
        assert response.status_code == status.HTTP_200_OK
        assert question_in_db == models.Question.parse_obj(response.json())


class TestGetAnswer(Base):
    _route_name = RoutsNames.GET_ANSWER

    async def test_get_if_exist(self, answer_in_db: models.Answer):
        response = await self.client.get(self.get_url(question_id="question", answer_id=answer_in_db.id))
        assert response.status_code == status.HTTP_200_OK
        assert answer_in_db == models.Answer.parse_obj(response.json())

    async def test_get_if_not_exist(self):
        response = await self.client.get(self.get_url(question_id="question", answer_id="wrong_id"))
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestCreateAnswer(Base):
    _route_name = RoutsNames.CREATE_ANSWER

    async def test_create_answer_if_not_exist(
        self,
        create_answer_command: commands.CreateAnswer,
        user_in_db: models.User,
        repository: AbstractRepository,
        question_in_db: models.Question,
    ):
        response = await self.client.post(
            self.get_url(question_id=question_in_db.id),
            params={"user_id": user_in_db.id},
            json=create_answer_command.dict(),
        )
        assert response.status_code == status.HTTP_201_CREATED
        answer = models.Answer.parse_obj(response.json())
        answer_from_db = await repository.get_answer_by_id(answer.id)
        assert answer == answer_from_db

    async def test_create_invalid_answer(
        self,
        create_answer_command: commands.CreateAnswer,
        user_in_db: models.User,
        repository: AbstractRepository,
        question_in_db: models.Question,
    ):
        create_answer_command.answer[0] = ("wrong", str(True))
        response = await self.client.post(
            self.get_url(question_id=question_in_db.id),
            params={"user_id": user_in_db.id},
            json=create_answer_command.dict(),
        )
        assert response.status_code == status.HTTP_409_CONFLICT

    async def test_create_answer_if_exist(
        self,
        create_answer_command: commands.CreateAnswer,
        user_in_db: models.User,
        answer_in_db: models.Answer,
        question_in_db: models.Question,
    ):
        response = await self.client.post(
            self.get_url(question_id=question_in_db.id),
            params={"user_id": user_in_db.id},
            json=create_answer_command.dict(),
        )
        assert response.status_code == status.HTTP_409_CONFLICT


class TestCreateTag(Base):
    _route_name = RoutsNames.CREATE_TAG

    async def test_create_tag(
        self,
        user_in_db: models.User,
        answer_in_db: models.Answer,
        question_in_db: models.Question,
        create_tag_command: commands.CreateTag,
    ):
        response = await self.client.post(
            self.get_url(question_id=question_in_db.id, answer_id=answer_in_db.id),
            params={"user_id": user_in_db.id},
            json=create_tag_command.dict(),
        )

        assert response.status_code == status.HTTP_201_CREATED
