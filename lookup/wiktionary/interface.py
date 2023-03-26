from typing import List, Type, Any

from core.types import Language, Card
from core.util import StatusOr
from lookup.interface import LookupInterface
from lookup.wiktionary.internal import interface_internals as internals
from lookup.wiktionary.languages import *


class WiktionaryInterface(LookupInterface):
    def __init__(self, answer_language: Language, target_language: Language):
        super(WiktionaryInterface, self).__init__(answer_language, target_language)
        # TODO: Change to multi-language support
        self.answer_parser = EnglishLocaleParser
        self.question_parser = GermanLocaleParser

    @staticmethod
    def _generic_lookup(text: str, source_parser: Type[LocalizedParser],
                        target_parser: Type[LocalizedParser]) -> StatusOr[Any]:
        source_articles_status = internals.get_source_definitions(
            text, source_parser, target_parser.language_codes_for_translations())
        if source_articles_status.is_error():
            return source_articles_status.to_other()

        source_lookup_data = internals.build_source_lookup_data(source_articles_status.value)
        # debug.maybe_print_source_lookup_data(source_lookup_data)

        full_lookup_data = internals.get_translations_and_build_full_lookup_data(
            source_lookup_data, target_parser)
        if full_lookup_data.is_error():
            return full_lookup_data.to_other()

        return StatusOr(full_lookup_data.value)

    def lookup_by_answer(self, text: str) -> StatusOr[List[Card]]:
        # debug.maybe_print_answer_input(text)

        translated_lookup_data_status = self._generic_lookup(text, self.answer_parser, self.question_parser)
        if translated_lookup_data_status.is_error():
            return translated_lookup_data_status.to_other()

        suggested_cards = internals.build_cards_from_answer_data(translated_lookup_data_status.value)
        # debug.maybe_print_suggested_cards(suggested_cards)

        return StatusOr(suggested_cards)

    def lookup_by_question(self, text: str) -> StatusOr[List[Card]]:
        # debug.maybe_print_question_input(text)

        translated_lookup_data_status = self._generic_lookup(text, self.question_parser, self.answer_parser)
        if translated_lookup_data_status.is_error():
            return translated_lookup_data_status.to_other()

        suggested_cards = internals.build_cards_from_question_data(translated_lookup_data_status.value)
        # debug.maybe_print_suggested_cards(suggested_cards)

        return StatusOr(suggested_cards)
