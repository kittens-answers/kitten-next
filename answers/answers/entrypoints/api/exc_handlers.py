from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from answers.domain.exceptions import repository_exc


def handle_repo_exc(request: Request, exc: repository_exc.RepositoryException):
    match exc:
        case repository_exc.QuestionDoesNotExist():
            return JSONResponse(content={"error": "question does not exist"}, status_code=status.HTTP_404_NOT_FOUND)
        case repository_exc.AnswerDoesNotExist():
            return JSONResponse(content={"error": "answer does not exist"}, status_code=status.HTTP_404_NOT_FOUND)
        case repository_exc.AnswerAlreadyExist():
            return JSONResponse(content={"error": "answer already exist"}, status_code=status.HTTP_409_CONFLICT)
        case repository_exc.AnswerCanNotBeAddedToQuestion():
            return JSONResponse(
                content={"error": "answer can not be added to question"}, status_code=status.HTTP_409_CONFLICT
            )
        case repository_exc.UserAlreadyExist():
            return JSONResponse(content={"error": "user already exist"}, status_code=status.HTTP_409_CONFLICT)
        case repository_exc.UserDoesNotExist():
            return JSONResponse(content={"error": "user does not exist"}, status_code=status.HTTP_404_NOT_FOUND)
        case repository_exc.QuestionAlreadyExist():
            return JSONResponse(content={"error": "question already exist"}, status_code=status.HTTP_409_CONFLICT)


def config_exc_handlers(app: FastAPI):
    app.add_exception_handler(repository_exc.RepositoryException, handle_repo_exc)
