from typing import List

from core.types import Language, Card
from core.util import StatusOr


class LookupInterface:
    def __init__(self, answer_language: Language, question_language: Language):
        self.answer_language = answer_language
        self.question_language = question_language

    def lookup_by_answer(self, text: str) -> StatusOr[List[Card]]:
        raise NotImplementedError

    def lookup_by_question(self, text: str) -> StatusOr[List[Card]]:
        raise NotImplementedError
