from typing import List, Type, Any

from core.types import Language, Card
from core.util import StatusOr
from lookup.interface import LookupInterface
from lookup.wiktionary import debug
from lookup.wiktionary.internal import interface_internals as internals
from lookup.wiktionary.languages import *


class WiktionaryInterface(LookupInterface):
    def __init__(self):
        # TODO: Change to multi-language support
        super(WiktionaryInterface, self).__init__(Language.EN, Language.DE)
        self.answer_parser = EnglishLocaleParser
        self.question_parser = GermanLocaleParser

    @staticmethod
    def _generic_lookup(text: str, source_parser: Type[LocalizedParser],
                        target_parser: Type[LocalizedParser]) -> StatusOr[Any]:
        source_definitions_status = internals.get_source_definitions(
            text, source_parser, target_parser.language_codes_for_translations())
        if source_definitions_status.is_error():
            return source_definitions_status.to_other()
        debug.maybe_print_source_definitions(source_definitions_status.value)

        source_lookup_data = internals.build_source_lookup_data(source_definitions_status.value)
        debug.maybe_print_source_data(source_lookup_data)

        full_lookup_data = internals.get_translations_and_build_full_lookup_data(
            source_lookup_data, target_parser)
        if full_lookup_data.is_error():
            return full_lookup_data.to_other()

        return StatusOr(full_lookup_data.value)

    def lookup_by_answer(self, text: str) -> StatusOr[List[Card]]:
        debug.maybe_print_answer_start(text)
        translated_lookup_data_status = self._generic_lookup(text, self.answer_parser, self.question_parser)
        if translated_lookup_data_status.is_error():
            return translated_lookup_data_status.to_other()

        suggested_cards = internals.build_cards_from_answer_data(translated_lookup_data_status.value)

        return StatusOr(suggested_cards)

    def lookup_by_question(self, text: str) -> StatusOr[List[Card]]:
        debug.maybe_print_question_start(text)
        translated_lookup_data_status = self._generic_lookup(text, self.question_parser, self.answer_parser)
        if translated_lookup_data_status.is_error():
            return translated_lookup_data_status.to_other()

        suggested_cards = internals.build_cards_from_question_data(translated_lookup_data_status.value)

        return StatusOr(suggested_cards)
