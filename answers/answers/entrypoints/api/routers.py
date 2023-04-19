from enum import StrEnum

from fastapi import APIRouter, FastAPI, status

from answers.domain import commands, models
from answers.entrypoints.api.dependencies import CurrentUser, Repository

router = APIRouter()


class RoutsNames(StrEnum):
    CREATE_QUESTION = "CREATE_QUESTION"
    GET_QUESTION = "GET_QUESTION"
    CREATE_ANSWER = "CREATE_ANSWER"
    GET_ANSWER = "GET_ANSWER"
    CREATE_TAG = "CREATE_TAG"
    GET_USER = "GET_USER"
    CREATE_USER = "CREATE_USER"


@router.get("/user/{user_id}", name=RoutsNames.GET_USER, response_model=models.User)
async def get_user(user_id: str, repository: Repository):
    return await repository.get_user_by_id(user_id=user_id)


@router.post("/user", name=RoutsNames.CREATE_USER, status_code=status.HTTP_201_CREATED, response_model=models.User)
async def create_user(repository: Repository, command: commands.CreateUser):
    return await repository.create_user(command=command)


@router.post(
    "/data", name=RoutsNames.CREATE_QUESTION, status_code=status.HTTP_201_CREATED, response_model=models.Question
)
async def create_question(user: CurrentUser, repository: Repository, dto: commands.CreateQuestion):
    return await repository.create_question(user=user, command=dto)


@router.get("/data/{question_id}", name=RoutsNames.GET_QUESTION, response_model=models.Question)
async def get_question_by_id(repository: Repository, question_id: str):
    return await repository.get_question_by_id(question_id)


@router.post(
    "/data/{question_id}",
    name=RoutsNames.CREATE_ANSWER,
    response_model=models.Answer,
    status_code=status.HTTP_201_CREATED,
)
async def create_answer(user: CurrentUser, repository: Repository, dto: commands.CreateAnswer, question_id: str):
    return await repository.create_answer(user=user, question_id=question_id, command=dto)


@router.get("/data/{question_id}/{answer_id}", name=RoutsNames.GET_ANSWER)
async def get_answer_by_id(repository: Repository, question_id: str, answer_id: str):
    return await repository.get_answer_by_id(answer_id=answer_id)


@router.post("/data/{question_id}/{answer_id}", name=RoutsNames.CREATE_TAG, status_code=status.HTTP_201_CREATED)
async def create_tag(
    repository: Repository,
    question_id: str,
    answer_id: str,
    user: CurrentUser,
    dto: commands.CreateTag,
):
    return await repository.add_tag(user=user, answer_id=answer_id, command=dto)


def config_routes(app: FastAPI):
    app.include_router(router=router)
