import itertools
from typing import List, Dict, Type, NamedTuple, Generator, Tuple

from core.types import Card
from core.util import StatusOr
from lookup.wiktionary.internal.markup_tree import build_wiki_content_tree
from lookup.wiktionary.internal.web_api import WebArticle, search_articles, retrieve_articles
from lookup.wiktionary.languages.base import LocalizedParser, WordDefinition, PartOfSpeech


def _extract_definitions_from_web_result(web_articles: List[WebArticle], parser: Type[LocalizedParser],
                                         translation_language_codes: List[str]) -> List[WordDefinition]:
    result_definitions = []
    for web_article in web_articles:
        markup_tree = build_wiki_content_tree(web_article.content, web_article.title)
        result_definitions.extend(
            parser.extract_word_definitions(markup_tree, web_article.title, translation_language_codes))
    return result_definitions


def get_source_definitions(text: str, parser: Type[LocalizedParser],
                           translation_language_codes: List[str]) -> StatusOr[List[WordDefinition]]:
    web_articles_status = search_articles(text, parser.api_language_code())
    if web_articles_status.is_error():
        return web_articles_status.to_other()
    return StatusOr(_extract_definitions_from_web_result(web_articles_status.value, parser, translation_language_codes))


class WordDefinitionKey(NamedTuple):
    wiki_title: str
    part_of_speech: PartOfSpeech

    def __str__(self):
        return 'WDKey {}-{}'.format(self.part_of_speech.name, self.wiki_title)


class SourceLookupData(NamedTuple):
    # Translated title + Source part of speech => Source word definition
    translated_words_to_sources: Dict[WordDefinitionKey, List[WordDefinition]]
    # List of unique wiki titles to look up based on |translated_words_to_sources|
    unique_translation_titles: List[str]


def build_source_lookup_data(definitions: List[WordDefinition]) -> SourceLookupData:
    _TRANSLATIONS_PER_DEFINITION_LIMIT = 6
    _DEFINITIONS_LIMIT = 5

    translated_words_to_sources: Dict[WordDefinitionKey, List[WordDefinition]] = dict()
    for definition in definitions[:_DEFINITIONS_LIMIT]:
        for translation_word in definition.translation_wiki_titles[:_TRANSLATIONS_PER_DEFINITION_LIMIT]:
            translated_word_key: WordDefinitionKey = WordDefinitionKey(translation_word, definition.part_of_speech)
            translated_words_to_sources.setdefault(translated_word_key, []).append(definition)

    all_translation_titles = [word_key.wiki_title for word_key in translated_words_to_sources.keys()]
    unique_translation_titles = list(set(all_translation_titles))
    return SourceLookupData(translated_words_to_sources, unique_translation_titles)


class FullLookupData(NamedTuple):
    # Preserved from |SourceLookupData|
    translated_words_to_sources: Dict[WordDefinitionKey, List[WordDefinition]]
    # Translated title + Source part of speech => Translated definition
    translated_words_to_translations: Dict[WordDefinitionKey, List[WordDefinition]]


def get_translations_and_build_full_lookup_data(
        source_lookup_data: SourceLookupData, parser: Type[LocalizedParser]) -> StatusOr[FullLookupData]:
    translation_web_articles_status = retrieve_articles(
        source_lookup_data.unique_translation_titles, parser.api_language_code())
    if translation_web_articles_status.is_error():
        return translation_web_articles_status.to_other()

    # We do not use translations section in translated articles to back-reference original definition, as they are
    # often disagree for various reasons.
    translated_definitions = _extract_definitions_from_web_result(translation_web_articles_status.value, parser, [])

    translated_words_to_translations: Dict[WordDefinitionKey, List[WordDefinition]] = dict()
    for translated_definition in translated_definitions:
        translation_key = WordDefinitionKey(translated_definition.wiki_title, translated_definition.part_of_speech)
        translated_words_to_translations.setdefault(translation_key, []).append(translated_definition)

    return StatusOr(FullLookupData(source_lookup_data.translated_words_to_sources, translated_words_to_translations))


# Generator, that takes dicts {translation_key => source_definitions} and {translation_key=>translated_definitions},
# matches them by key, and yields all possible pairs of source definition and translation definition.
def _join_sources_to_translations(
        full_lookup_data: FullLookupData) -> Generator[Tuple[WordDefinition, WordDefinition], None, None]:
    for translation_word_key in full_lookup_data.translated_words_to_sources.keys():
        if translation_word_key not in full_lookup_data.translated_words_to_translations:
            continue
        source_definitions = full_lookup_data.translated_words_to_sources[translation_word_key]
        translated_definitions = full_lookup_data.translated_words_to_translations[translation_word_key]

        for source, translation in itertools.product(source_definitions, translated_definitions):
            assert source.part_of_speech == translation.part_of_speech
            yield source, translation


def build_cards_from_answer_data(full_lookup_data: FullLookupData) -> List[Card]:
    cards: List[Card] = []
    # Based on knowledge that source definitions should be used in meaning_note and answer fields.
    for source_definition, translation_definition in _join_sources_to_translations(full_lookup_data):
        cards.append(Card(
            card_type=source_definition.part_of_speech,
            question=translation_definition.word_readable,
            question_grammar_forms=translation_definition.grammar_forms,
            answer=source_definition.word_readable,
            note=source_definition.meaning_note
        ))
    return cards


def build_cards_from_question_data(full_lookup_data: FullLookupData) -> List[Card]:
    cards: List[Card] = []
    # Based on knowledge that translated definitions should be used in meaning_note and answer fields.
    for source_definition, translation_definition in _join_sources_to_translations(full_lookup_data):
        cards.append(Card(
            card_type=source_definition.part_of_speech,
            question=source_definition.word_readable,
            question_grammar_forms=source_definition.grammar_forms,
            answer=translation_definition.word_readable,
            note=translation_definition.meaning_note
        ))
    return cards
