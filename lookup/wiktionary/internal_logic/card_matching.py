from enum import Enum
from typing import List, Generator, Tuple

from core.types import Card
from lookup.wiktionary.internal_logic.debug import debug_print_matching
from lookup.wiktionary.types import Definition, DefinitionSet, DefinitionSetKey


class DTCMatchingType(Enum):
    AnswerBased = 1
    QuestionBased = 2


class DefinitionsToCardsMatcher:
    @classmethod
    def _card_from_definitions(cls, answer_definition: Definition, translated_definition: Definition) -> Card:
        return Card(
            card_type=answer_definition.part_of_speech,
            answer=answer_definition.readable_name,
            question=translated_definition.readable_name,
            grammar_note=translated_definition.grammar_note,
            meaning_note=answer_definition.meaning_note
        )

    @classmethod
    def _all_definitions(cls, definition_set: DefinitionSet) -> Generator[Definition, None, None]:
        for definitions_list in definition_set.values():
            for definition in definitions_list:
                yield definition

    @classmethod
    def _extract_full_matches(cls, source_set: DefinitionSet, translated_set: DefinitionSet,
                              source_is_answers: bool) -> Tuple[List[Card], List[Definition]]:
        fully_matched_cards: List[Card] = []
        unmatched_definitions: List[Definition] = []
        for definition in cls._all_definitions(source_set):
            match_found = False
            for translated_key_title in definition.translation_articles:
                translated_key = DefinitionSetKey(translated_key_title, definition.part_of_speech)
                if translated_key not in translated_set:
                    continue
                for translated_definition in translated_set[translated_key]:
                    if definition.raw_article_title not in translated_definition.translation_articles:
                        continue
                    match_found = True
                    fully_matched_cards.append(cls._card_from_definitions(
                        answer_definition=definition if source_is_answers else translated_definition,
                        translated_definition=translated_definition if source_is_answers else definition))
            if not match_found:
                unmatched_definitions.append(definition)
        return fully_matched_cards, unmatched_definitions

    @classmethod
    def _extract_one_side_matches(cls, unmatched_definitions: List[Definition], translated_set: DefinitionSet,
                                  source_is_answers: bool) -> List[Card]:
        results: List[Card] = []
        for definition in unmatched_definitions:
            for translated_key_title in definition.translation_articles:
                translated_key = DefinitionSetKey(translated_key_title, definition.part_of_speech)
                if translated_key not in translated_set:
                    continue
                for translated_definition in translated_set[translated_key]:
                    results.append(cls._card_from_definitions(
                        answer_definition=definition if source_is_answers else translated_definition,
                        translated_definition=translated_definition if source_is_answers else definition))
        return results

    @classmethod
    def create_cards(cls, matching_type: DTCMatchingType,
                     answer_definition_set: DefinitionSet, question_definition_set: DefinitionSet) -> List[Card]:
        matched_from_answer, unmatched_from_answer = cls._extract_full_matches(
            answer_definition_set, question_definition_set, source_is_answers=True)
        matched_from_question, unmatched_from_question = cls._extract_full_matches(
            question_definition_set, answer_definition_set, source_is_answers=False)

        additional_from_answer = cls._extract_one_side_matches(
            unmatched_from_answer, question_definition_set, source_is_answers=True)
        additional_from_question = cls._extract_one_side_matches(
            unmatched_from_question, answer_definition_set, source_is_answers=False)

        debug_print_matching(answer_definition_set, question_definition_set,
                             matched_from_question, matched_from_question,
                             additional_from_answer, additional_from_question)

        if matching_type == DTCMatchingType.AnswerBased:
            return matched_from_question + additional_from_question + additional_from_answer
        return matched_from_answer + additional_from_answer + additional_from_question
