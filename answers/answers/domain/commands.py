from dataclasses import dataclass

from answers.domain.models import QuestionType


def is_only_uniq_items_list(_list: list) -> bool:
    return len(_list) == len(set(_list))


@dataclass()
class CreateQuestion:
    question_text: str
    question_type: QuestionType
    options: list[str]
    extra_options: list[str]

    def validate(self):
        if not self.question_text:
            raise ValueError
        if not all(self.options):
            raise ValueError
        if not all(self.extra_options):
            raise ValueError
        match self.question_type:
            case QuestionType.ONE | QuestionType.MANY:
                if self.extra_options:
                    raise ValueError
                if self.options and len(self.options) < 2:
                    raise ValueError
            case QuestionType.ORDER:
                if self.extra_options:
                    raise ValueError
                if len(self.options) < 2:
                    raise ValueError
            case QuestionType.MATCH:
                if len(self.extra_options) < 2:
                    raise ValueError
                if len(self.extra_options) != len(self.options):
                    raise ValueError


@dataclass()
class CreateAnswer:
    question_id: str
    answer: list[tuple[str, str]]

    @property
    def left_answers(self):
        return list(x[0] for x in self.answer)

    @property
    def right_answers(self):
        return list(x[1] for x in self.answer)

    def validate(self, question: CreateQuestion):
        if not is_only_uniq_items_list(self.left_answers):
            raise ValueError
        match question.question_type:
            case QuestionType.ONE:
                if len(self.answer) != 1:
                    raise ValueError

            case QuestionType.MANY:
                ...
            case QuestionType.ORDER:
                ...
            case QuestionType.MATCH:
                ...
