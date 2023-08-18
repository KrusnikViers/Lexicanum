from typing import List

from core.types import Language, Card
from core.util import StatusOr
from lookup.interface import LookupInterface
from lookup.wiktionary.internal_logic import match_definition_sets, lookup_definition_sets
from lookup.wiktionary.languages import EnglishLocaleParser, GermanLocaleParser
from lookup.wiktionary.internal_logic.debug import debug_event_timer, debug_reset_timer


class WiktionaryInterface(LookupInterface):
    def __init__(self):
        # TODO: Change to multi-language support
        super().__init__(Language.EN, Language.DE)
        self.answer_parser = EnglishLocaleParser
        self.question_parser = GermanLocaleParser

    def lookup_by_answer(self, text: str) -> StatusOr[List[Card]]:
        debug_reset_timer()
        lookup_status = lookup_definition_sets(
            text, source_parser=self.answer_parser, translations_parser=self.question_parser)
        if lookup_status.is_error():
            return lookup_status.to_other()
        answers_set, questions_set = lookup_status.value

        cards_list = match_definition_sets(answers_set, questions_set, order_by_question=False)
        if not cards_list:
            return StatusOr(status="No cards could be constructed")
        debug_event_timer("cards ready")
        return StatusOr(cards_list)

    def lookup_by_question(self, text: str) -> StatusOr[List[Card]]:
        debug_reset_timer()
        lookup_status = lookup_definition_sets(
            text, source_parser=self.question_parser, translations_parser=self.answer_parser)
        if lookup_status.is_error():
            return lookup_status.to_other()
        questions_set, answers_set = lookup_status.value

        cards_list = match_definition_sets(answers_set, questions_set, order_by_question=True)
        if not cards_list:
            return StatusOr(status="No cards could be constructed")
        debug_event_timer("cards ready")
        return StatusOr(cards_list)
