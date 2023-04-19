from answers.domain import models


class RepositoryException(Exception):
    ...


class UserDoesNotExist(RepositoryException):
    def __init__(self, user_id: str) -> None:
        self.user_id = user_id


class UserAlreadyExist(RepositoryException):
    def __init__(self, user: models.User) -> None:
        self.user = user


class QuestionDoesNotExist(RepositoryException):
    def __init__(self, question_id: str) -> None:
        self.question_id = question_id


class QuestionAlreadyExist(RepositoryException):
    def __init__(self, question: models.Question) -> None:
        self.question = question


class AnswerDoesNotExist(RepositoryException):
    def __init__(self, answer_id: str) -> None:
        self.answer_id = answer_id


class AnswerAlreadyExist(RepositoryException):
    def __init__(self, answer: models.Answer) -> None:
        self.answer = answer


class AnswerCanNotBeAddedToQuestion(RepositoryException):
    ...


class TagAlreadyExist(RepositoryException):
    ...
