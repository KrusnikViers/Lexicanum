from typing import List, Type

from core.types import Language
from core.util import StatusOr
from lookup.interface import LookupEngine, LookupRequest, LookupResponse
from lookup.wiktionary.internal import web_api
from lookup.wiktionary.internal.markup import build_wiki_content_tree
from lookup.wiktionary.languages import *

_SUPPORTED_LOCALES = {
    Language.EN: EnglishLocaleParser,
    Language.DE: GermanLocaleParser,
}


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


def _lookup_from_answer(request: LookupRequest) -> StatusOr[LookupResponse]:
    source_parser = _SUPPORTED_LOCALES[request.source_language]
    target_parser = _SUPPORTED_LOCALES[request.target_language]

    source_articles_status = _search_for_definitions(request.text, source_parser,
                                                     target_parser.translation_language_codes())
    if not source_articles_status.is_ok():
        return source_articles_status.to_other()

    print('\n\n========================\n\n'.join(map(str, source_articles_status.value)))
    return StatusOr(status='Not Implemented')


def _lookup_from_question(request: LookupRequest) -> StatusOr[LookupResponse]:
    source_parser = _SUPPORTED_LOCALES[request.source_language]
    target_parser = _SUPPORTED_LOCALES[request.target_language]

    source_articles_status = _search_for_definitions(request.text, source_parser,
                                                     target_parser.translation_language_codes())
    if not source_articles_status.is_ok():
        return source_articles_status.to_other()

    print('\n\n========================\n\n'.join(map(str, source_articles_status.value)))
    return StatusOr(status='Not Implemented')


class WiktionaryLookupEngine(LookupEngine):
    def lookup(self, request: LookupRequest) -> StatusOr[LookupResponse]:
        if request.source_type == LookupRequest.Type.ANSWER:
            return _lookup_from_answer(request)
        if request.source_type == LookupRequest.Type.QUESTION:
            return _lookup_from_question(request)
        raise ValueError
