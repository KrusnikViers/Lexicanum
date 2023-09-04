from typing import List

from lookup.wiktionary.languages.base.definitions_composer import DefinitionsComposer
from lookup.wiktionary.types import DefinitionComponent, MarkupTree, Definition, DebugInterface


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
    def extract_definitions(cls, markup_tree: MarkupTree, source_wiki_title: str,
                            language_codes_for_translations: List[str],
                            debug_interface: DebugInterface | None = None) -> List[Definition]:
        components_list = cls.extract_definition_components(markup_tree, source_wiki_title,
                                                            language_codes_for_translations)
        if debug_interface:
            debug_interface.show_components_list(source_wiki_title, cls.api_language_code(), components_list)
        definitions_composer = DefinitionsComposer(source_wiki_title, language_codes_for_translations)
        return definitions_composer.build(components_list)

    # Building definitions from components expected to be the same for all languages.
    @classmethod
    def extract_definition_components(cls, markup_tree: MarkupTree, source_wiki_title: str,
                                      language_codes_for_translations: List[str]) -> List[DefinitionComponent]:
        raise NotImplementedError
