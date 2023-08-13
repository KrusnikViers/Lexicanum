from typing import List

from lookup.wiktionary.types.definition_components import DefinitionComponent
from lookup.wiktionary.types.markup_tree import MarkupTree


# Every language parsing package should implement this class as an outside interface.
class LocalizedParser:
    @classmethod
    # Language code to access Wiktionary localized endpoint.
    def api_language_code(cls) -> str:
        raise NotImplementedError

    @classmethod
    # Used for extracting translations from the wiki page. Usually just main language code, but multiple language codes
    # can be suitable as well (e.g. 'high' and 'common' version of the same language).
    def language_codes_for_translations(cls) -> List[str]:
        raise NotImplementedError

    @classmethod
    def extract_definition_components(cls, markup_tree: MarkupTree, source_wiki_title: str,
                                      language_codes_for_translations: List[str]) -> List[DefinitionComponent]:
        raise NotImplementedError
