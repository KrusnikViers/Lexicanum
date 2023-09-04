from typing import List, Type, Tuple

from core.util import StatusOr
from lookup.wiktionary.internal_logic.web_api import WebArticle, search_articles, retrieve_articles
from lookup.wiktionary.languages import LocalizedParser
from lookup.wiktionary.types import DefinitionSet, build_definition_set, MarkupTree, DebugInterface


def _articles_to_definition_set(articles: List[WebArticle],
                                article_parser: Type[LocalizedParser],
                                translations_parser: Type[LocalizedParser],
                                debug_interface: DebugInterface | None) -> DefinitionSet:
    extracted_definitions = []
    for article in articles:
        markup_tree = MarkupTree.build(article.title, article.content)
        extracted_definitions += article_parser.extract_definitions(
            markup_tree, article.title, translations_parser.language_codes_for_translations(), debug_interface)
        if debug_interface:
            debug_interface.show_raw_wiki_content(article.title, article_parser.api_language_code(), article.content)
            debug_interface.show_markup_tree(article.title, article_parser.api_language_code(), markup_tree)
    return build_definition_set(extracted_definitions)


def lookup_definition_sets(
        search_text: str,
        source_parser: Type[LocalizedParser],
        translations_parser: Type[LocalizedParser],
        debug_interface: DebugInterface | None) -> StatusOr[Tuple[DefinitionSet, DefinitionSet]]:
    # Fetch source articles
    source_articles_status = search_articles(search_text, source_parser.api_language_code())
    if source_articles_status.is_error():
        if debug_interface:
            debug_interface.progress_rich_message('Source articles lookup error', source_articles_status.status)
        return source_articles_status.to_other()

    # Create source definition set and list of translation titles
    source_definition_set = _articles_to_definition_set(source_articles_status.value,
                                                        source_parser, translations_parser, debug_interface)
    unique_translation_titles = list(set([title
                                          for definitions_list in source_definition_set.values()
                                          for definition in definitions_list
                                          for title in definition.translation_articles]))
    if not unique_translation_titles:
        return StatusOr(status="Not enough data extracted from search request")

    # Fetch translation articles
    translation_articles_status = retrieve_articles(unique_translation_titles,
                                                    translations_parser.api_language_code())
    if translation_articles_status.is_error():
        return translation_articles_status.to_other()

    # Create translations definition set
    translation_definition_set = _articles_to_definition_set(translation_articles_status.value,
                                                             translations_parser, source_parser, debug_interface)
    return StatusOr((source_definition_set, translation_definition_set))
