from typing import List

from core.types import Language, Card
from core.util import StatusOr
from lookup.interface import LookupInterface
from lookup.wiktionary.internal_logic import DefinitionsToCardsMatcher, DTCMatchingType, lookup_definition_sets
from lookup.wiktionary.languages import EnglishLocaleParser, GermanLocaleParser


class WiktionaryInterface(LookupInterface):
    def __init__(self):
        # TODO: Change to multi-language support
        super().__init__(Language.EN, Language.DE)
        self.answer_parser = EnglishLocaleParser
        self.question_parser = GermanLocaleParser

    def lookup_by_answer(self, text: str) -> StatusOr[List[Card]]:
        lookup_status = lookup_definition_sets(
            text, source_parser=self.answer_parser, translations_parser=self.question_parser)
        if lookup_status.is_error():
            return lookup_status.to_other()
        answers_set, questions_set = lookup_status.value

        cards_list = DefinitionsToCardsMatcher.create_cards(DTCMatchingType.AnswerBased, answers_set, questions_set)
        if not cards_list:
            return StatusOr(status="No cards could be constructed")
        return StatusOr(cards_list)

    def lookup_by_question(self, text: str) -> StatusOr[List[Card]]:
        lookup_status = lookup_definition_sets(
            text, source_parser=self.question_parser, translations_parser=self.answer_parser)
        if lookup_status.is_error():
            return lookup_status.to_other()
        questions_set, answers_set = lookup_status.value

        cards_list = DefinitionsToCardsMatcher.create_cards(DTCMatchingType.QuestionBased, answers_set, questions_set)
        if not cards_list:
            return StatusOr(status="No cards could be constructed")
        return StatusOr(cards_list)
