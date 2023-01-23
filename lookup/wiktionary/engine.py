import itertools
from collections import namedtuple
from typing import List, Type, Dict

from core.types import Language, Card
from core.util import StatusOr, if_none
from lookup.interface import LookupEngine, LookupRequest, LookupResponse
from lookup.wiktionary.debug import *
from lookup.wiktionary.internal import web_api
from lookup.wiktionary.internal.markup import build_wiki_content_tree
from lookup.wiktionary.languages import *

_SUPPORTED_LOCALES = {
    Language.EN: EnglishLocaleParser,
    Language.DE: GermanLocaleParser,
}

_WordWithType = namedtuple("_WordWithType", "word part_of_speech")
_TranslationMeta = namedtuple("_TranslationMeta", "meaning_note original_definition")
_SearchableTranslation = namedtuple("_SearchableTranslation", "word_with_type translation_meta")


def _definitions_from_web_articles(
        web_articles: List[web_api.WebArticle],
        source_parser: Type[WiktionaryLocalizedParser],
        target_parser: Type[WiktionaryLocalizedParser] | None = None) -> List[WiktionaryWordDefinition]:
    definitions = []
    for web_article in web_articles:
        markup_tree = build_wiki_content_tree(web_article.content, web_article.title)
        definitions += source_parser.extract_word_definitions(markup_tree, web_article.title, target_parser)
    return definitions


def _create_unique_translations_dict(
        definitions: List[WiktionaryWordDefinition]) -> Dict[_WordWithType, _TranslationMeta]:
    result: Dict[_WordWithType, _TranslationMeta] = {}
    all_searchable_translations: List[_SearchableTranslation] = []
    for definition in definitions:
        for definition_translations_set in definition.translations:
            all_searchable_words = itertools.chain(*definition_translations_set.translations.values())
            for word in all_searchable_words:
                all_searchable_translations.append(_SearchableTranslation(
                    _WordWithType(word, definition.card_type),
                    _TranslationMeta(definition_translations_set.meaning_note, definition)))
    for searchable_definition in all_searchable_translations:
        if searchable_definition.word_with_type in result and result[searchable_definition.word_with_type].meaning_note:
            continue
        result[searchable_definition.word_with_type] = searchable_definition.translation_meta
    return result


def _search_definitions(
        search_word: str,
        source_parser: Type[WiktionaryLocalizedParser],
        target_parser: Type[WiktionaryLocalizedParser] | None) -> StatusOr[List[WiktionaryWordDefinition]]:
    _web_articles_status = web_api.search_articles(search_word, source_parser.endpoint_language_code())
    if not _web_articles_status.is_ok():
        return _web_articles_status.to_other()
    return StatusOr(_definitions_from_web_articles(_web_articles_status.value, source_parser, target_parser))


def _retrieve_definitions_for_translations_dict(
        translations_dict: Dict[_WordWithType, _TranslationMeta],
        translations_parser: Type[WiktionaryLocalizedParser]) -> StatusOr[List[WiktionaryWordDefinition]]:
    unique_titles_list = list(set([word_with_type.word for word_with_type in translations_dict.keys()]))
    _web_articles_status = web_api.retrieve_articles(unique_titles_list, translations_parser.endpoint_language_code())
    if not _web_articles_status.is_ok():
        return _web_articles_status.to_other()
    return StatusOr(_definitions_from_web_articles(_web_articles_status.value, source_parser=translations_parser))


def _print_wiki_contents(request, source_articles_status, retrieved_translations_status):
    print('=======Extracted wiki content for {}:{} lookup >>'.format(request.source_language.name, request.text))
    print('Articles fetched:')
    for article in source_articles_status.value:
        print(article)
    print('Translations fetched:')
    for article in retrieved_translations_status.value:
        print(article)
    print('=======Extracted wiki content for {}:{} lookup <<\n'.format(request.source_language.name, request.text))


def _lookup_from_answer(request: LookupRequest) -> StatusOr[LookupResponse]:
    if PRINT_LOOKUP_INPUTS:
        print('=====Looking up {} ...'.format(request))

    answer_parser = _SUPPORTED_LOCALES[request.source_language]
    question_parser = _SUPPORTED_LOCALES[request.target_language]

    source_articles_status = _search_definitions(
        request.text, source_parser=answer_parser, target_parser=question_parser)
    if not source_articles_status.is_ok():
        return source_articles_status.to_other()

    source_translations_dict = _create_unique_translations_dict(source_articles_status.value)
    retrieved_translations_status = _retrieve_definitions_for_translations_dict(
        source_translations_dict, question_parser)
    if not retrieved_translations_status.is_ok():
        return retrieved_translations_status.to_other()

    if PRINT_WIKICONTENTS:
        _print_wiki_contents(request, source_articles_status, retrieved_translations_status)

    result: List[Card] = []
    for retrieved_translation in retrieved_translations_status.value:
        translation_key = _WordWithType(retrieved_translation.wiki_title, retrieved_translation.card_type)
        if translation_key not in source_translations_dict:
            continue
        source_meta = source_translations_dict[translation_key]
        result.append(Card(retrieved_translation.card_type,
                           question=retrieved_translation.grammar_text,
                           answer=source_meta.original_definition.short_text,
                           note=if_none(source_meta.meaning_note, '')))

    if PRINT_CARDS:
        print('========Extracted cards for {}:{} lookup >>'.format(request.source_language.name, request.text))
        for card in result:
            print(card)
        print('========Extracted cards for {}:{} lookup <<'.format(request.source_language.name, request.text))

    return StatusOr(LookupResponse(result, request))


def _lookup_from_question(request: LookupRequest) -> StatusOr[LookupResponse]:
    if PRINT_LOOKUP_INPUTS:
        print('=====Looking up {} ...'.format(request))

    question_parser = _SUPPORTED_LOCALES[request.source_language]
    answer_parser = _SUPPORTED_LOCALES[request.target_language]

    source_articles_status = _search_definitions(
        request.text, source_parser=question_parser, target_parser=answer_parser)
    if not source_articles_status.is_ok():
        return source_articles_status.to_other()

    source_translations_dict = _create_unique_translations_dict(source_articles_status.value)
    retrieved_translations_status = _retrieve_definitions_for_translations_dict(source_translations_dict, answer_parser)
    if not retrieved_translations_status.is_ok():
        return retrieved_translations_status.to_other()

    if PRINT_WIKICONTENTS:
        _print_wiki_contents(request, source_articles_status, retrieved_translations_status)

    result: List[Card] = []
    for retrieved_translation in retrieved_translations_status.value:
        translation_key = _WordWithType(retrieved_translation.wiki_title, retrieved_translation.card_type)
        if translation_key not in source_translations_dict:
            continue
        source_meta = source_translations_dict[translation_key]
        result.append(Card(retrieved_translation.card_type,
                           question=source_meta.original_definition.grammar_text,
                           answer=retrieved_translation.short_text,
                           note=if_none(source_meta.meaning_note, '')))

    if PRINT_CARDS:
        print('========Extracted cards for {}:{} lookup >>'.format(request.source_language.name, request.text))
        for card in result:
            print(card)
        print('========Extracted cards for {}:{} lookup <<'.format(request.source_language.name, request.text))

    return StatusOr(LookupResponse(result, request))


class WiktionaryLookupEngine(LookupEngine):
    def lookup(self, request: LookupRequest) -> StatusOr[LookupResponse]:
        if request.source_type == LookupRequest.Type.ANSWER:
            result_status = _lookup_from_answer(request)
        elif request.source_type == LookupRequest.Type.QUESTION:
            result_status = _lookup_from_question(request)
        else:
            raise ValueError
        return result_status
