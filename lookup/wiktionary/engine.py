from typing import Type, Set, Dict, List

from core.types import Language
from core.util import StatusOr
from lookup.interface import LookupEngine, LookupRequest, LookupResponse
from lookup.wiktionary.language_support import *
from lookup.wiktionary.web_api import RequestedArticle

_SUPPORTED_LOCALES = {
    Language.EN: EnglishLocaleParser,
    Language.DE: GermanLocaleParser,
}


class WiktionaryLookupEngine(LookupEngine):
    @classmethod
    def _articles_list(cls, search_text: str,
                       language_parser: Type[WiktionaryLocaleParser]) -> StatusOr[List[WiktionaryArticle]]:
        fetched_articles: Dict[str, List[WiktionaryArticle]] = dict()
        fetched_search_words: Set[str] = set()
        see_also: List[str] = [search_text]

        while see_also:
            current_word = see_also.pop(-1)
            fetched_search_words.add(current_word)

            web_request_status = language_parser.get_articles_for(current_word)
            if not web_request_status.is_ok():
                if not see_also and not fetched_articles:
                    return web_request_status.to_other()
                continue

            parsed_articles = [article
                               for requested_article in web_request_status.value
                               for article in language_parser.parse_raw_article(requested_article)]
            for parsed_article in parsed_articles:
                fetched_articles.get(parsed_article.title, default=[]).append(parsed_article)
                for see_also_keyword in parsed_article.see_also:
                    if see_also_keyword not in see_also and \
                            see_also_keyword not in fetched_articles and \
                            see_also_keyword not in fetched_search_words:
                        see_also.append(see_also_keyword)

        return StatusOr(value=[article
                               for fetched_articles_list in fetched_articles.values()
                               for article in fetched_articles_list])

    @classmethod
    def _lookup_from_answer(cls, request: LookupRequest) -> StatusOr[LookupResponse]:
        source_parser = _SUPPORTED_LOCALES[request.source_language]
        target_parser = _SUPPORTED_LOCALES[request.target_language]

        source_articles_status = cls._articles_list(request.text, source_parser)
        if not source_articles_status.is_ok():
            return source_articles_status.to_other()
        print(source_articles_status.value)
        return StatusOr(status='Not Implemented')

    def lookup(self, request: LookupRequest) -> StatusOr[LookupResponse]:
        if request.source_type == LookupRequest.Type.ANSWER:
            return self._lookup_from_answer(request)
        raise NotImplementedError
