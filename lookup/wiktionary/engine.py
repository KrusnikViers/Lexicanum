import itertools
from collections import namedtuple
from typing import List, Type, Dict

from core.types import Language, Card
from core.util import StatusOr, if_none
from lookup.interface import LookupEngine, LookupRequest, LookupResponse
from lookup.wiktionary.internal import web_api
from lookup.wiktionary.internal.markup import build_wiki_content_tree
from lookup.wiktionary.languages import *

_SUPPORTED_LOCALES = {
    Language.EN: EnglishLocaleParser,
    Language.DE: GermanLocaleParser,
}

_Translation = namedtuple("_Translation", "word part_of_speech")
_TranslationMeta = namedtuple("_TranslationMeta", "meaning_note original_definition")


def _extract_definitions_from_plain_articles(plain_articles: List[web_api.RawWiktionaryArticle],
                                             localized_parser: Type[WiktionaryLocalizedParser],
                                             target_translation_codes: List[str]) -> List[WiktionaryWordDefinition]:
    definitions = []
    for plain_article in plain_articles:
        content_tree = build_wiki_content_tree(plain_article.content, plain_article.title)
        definitions += localized_parser.extract_word_definitions(
            content_tree, wiki_title=plain_article.title, target_translation_language_codes=target_translation_codes)
    return definitions


def _search_for_definitions(search_word: str, localized_parser: Type[WiktionaryLocalizedParser],
                            target_translation_codes: List[str]) -> StatusOr[List[WiktionaryWordDefinition]]:
    _plain_text_articles_status = web_api.search_for_articles(search_word, localized_parser.endpoint_language_code())
    if not _plain_text_articles_status.is_ok():
        return _plain_text_articles_status.to_other()
    return StatusOr(value=_extract_definitions_from_plain_articles(
        _plain_text_articles_status.value, localized_parser, target_translation_codes))


def _retrieve_definitions(titles: List[str], localized_parser: Type[WiktionaryLocalizedParser],
                          target_translation_codes: List[str]) -> StatusOr[List[WiktionaryWordDefinition]]:
    _plain_text_articles_status = web_api.retrieve_articles(titles, localized_parser.endpoint_language_code())
    if not _plain_text_articles_status.is_ok():
        return _plain_text_articles_status.to_other()
    return StatusOr(value=_extract_definitions_from_plain_articles(
        _plain_text_articles_status.value, localized_parser, target_translation_codes))


def _create_translations_dict(definitions: List[WiktionaryWordDefinition]) -> Dict[_Translation, _TranslationMeta]:
    result: Dict[_Translation, _TranslationMeta] = {}
    for definition in definitions:
        for meaning in definition.translations:
            unique_words = set(itertools.chain(*meaning.translations.values()))
            for word in unique_words:
                translation = _Translation(word, definition.card_type)
                if word in result and result[translation].meaning_note:
                    continue
                result[translation] = _TranslationMeta(meaning.meaning_note, definition)
    return result


def _lookup_from_answer(request: LookupRequest) -> StatusOr[LookupResponse]:
    answer_parser = _SUPPORTED_LOCALES[request.source_language]
    question_parser = _SUPPORTED_LOCALES[request.target_language]

    source_articles_status = _search_for_definitions(request.text, answer_parser,
                                                     question_parser.translation_language_codes())
    if not source_articles_status.is_ok():
        return source_articles_status.to_other()

    source_translations_dict = _create_translations_dict(source_articles_status.value)
    retrieved_translations = _retrieve_definitions(
        [translation.word for translation in source_translations_dict.keys()],
        question_parser, target_translation_codes=[])
    if not retrieved_translations.is_ok():
        return retrieved_translations.to_other()

    result: List[Card] = []
    for retrieved_translation in retrieved_translations.value:
        translation_key = _Translation(retrieved_translation.wiki_title, retrieved_translation.card_type)
        if translation_key not in source_translations_dict:
            continue
        source_meta = source_translations_dict[translation_key]
        result.append(Card(retrieved_translation.card_type,
                           question=retrieved_translation.grammar_string,
                           answer=source_meta.original_definition.short_title,
                           note=if_none(source_meta.meaning_note, '')))

    return StatusOr(LookupResponse(result, request))


def _lookup_from_question(request: LookupRequest) -> StatusOr[LookupResponse]:
    question_parser = _SUPPORTED_LOCALES[request.source_language]
    answer_parser = _SUPPORTED_LOCALES[request.target_language]

    source_articles_status = _search_for_definitions(request.text, question_parser,
                                                     answer_parser.translation_language_codes())
    if not source_articles_status.is_ok():
        return source_articles_status.to_other()

    source_translations_dict = _create_translations_dict(source_articles_status.value)
    retrieved_translations = _retrieve_definitions(
        [translation.word for translation in source_translations_dict.keys()],
        answer_parser, target_translation_codes=[])
    if not retrieved_translations.is_ok():
        return retrieved_translations.to_other()

    result: List[Card] = []
    for retrieved_translation in retrieved_translations.value:
        translation_key = _Translation(retrieved_translation.wiki_title, retrieved_translation.card_type)
        if translation_key not in source_translations_dict:
            continue
        source_meta = source_translations_dict[translation_key]
        result.append(Card(retrieved_translation.card_type,
                           question=source_meta.original_definition.short_title,
                           answer=retrieved_translation.grammar_string,
                           note=if_none(source_meta.meaning_note, '')))

    return StatusOr(LookupResponse(result, request))


class WiktionaryLookupEngine(LookupEngine):
    def lookup(self, request: LookupRequest) -> StatusOr[LookupResponse]:
        if request.source_type == LookupRequest.Type.ANSWER:
            return _lookup_from_answer(request)
        if request.source_type == LookupRequest.Type.QUESTION:
            return _lookup_from_question(request)
        raise ValueError
