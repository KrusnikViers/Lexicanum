from core.types import Language
from core.util import StatusOr
from lookup.interface import LookupEngine, LookupRequest, LookupResponse
from lookup.wiktionary.languages import *

_SUPPORTED_LOCALES = {
    Language.EN: EnglishLocaleParser,
    Language.DE: GermanLocaleParser,
}


class WiktionaryLookupEngine(LookupEngine):
    @classmethod
    def _lookup_from_answer(cls, request: LookupRequest) -> StatusOr[LookupResponse]:
        source_parser = _SUPPORTED_LOCALES[request.source_language]
        target_parser = _SUPPORTED_LOCALES[request.target_language]

        source_articles_status = source_parser.search_for_definitions(
            request.text, target_parser.translation_language_codes())
        if not source_articles_status.is_ok():
            return source_articles_status.to_other()

        print('\n\n========================\n\n'.join(map(str, source_articles_status.value)))
        return StatusOr(status='Not Implemented')

    @classmethod
    def _lookup_from_question(cls, request: LookupRequest) -> StatusOr[LookupResponse]:
        source_parser = _SUPPORTED_LOCALES[request.source_language]
        target_parser = _SUPPORTED_LOCALES[request.target_language]

        source_articles_status = source_parser.search_for_definitions(
            request.text, target_parser.translation_language_codes())
        if not source_articles_status.is_ok():
            return source_articles_status.to_other()

        print('\n\n========================\n\n'.join(map(str, source_articles_status.value)))
        return StatusOr(status='Not Implemented')

    def lookup(self, request: LookupRequest) -> StatusOr[LookupResponse]:
        if request.source_type == LookupRequest.Type.ANSWER:
            return self._lookup_from_answer(request)
        if request.source_type == LookupRequest.Type.QUESTION:
            return self._lookup_from_question(request)
        raise ValueError
