import itertools
from typing import List

from core.types import CardType
from core.util import StatusOr
from lookup.wiktionary.internal import WikitextContentNode, fetch_and_parse_matching_articles, fetch_and_parse_articles
from lookup.wiktionary.languages.base import WiktionaryWordDefinition, WiktionaryTranslations, WiktionaryLocalizedParser


def _maybe_get_translations(section: WikitextContentNode, target_translation_language_codes: List[str]) -> []:
    results = []
    for node in section.children:
        if node.name in ('Ü', 'Üxx4', 'Üt') and node.plain_args[0] in target_translation_language_codes:
            if not len(results):
                results.append(WiktionaryTranslations())
            language_code = node.plain_args[0]
            translations = results[-1].translations
            if language_code not in translations:
                translations[language_code] = [node.plain_args[1]]
            else:
                translations[language_code].append(node.plain_args[1])
    meaningful_results = [translation for translation in results if len(translation.translations)]

    for child_node in section.children:
        meaningful_results += _maybe_get_translations(child_node, target_translation_language_codes)
    return meaningful_results


def _maybe_get_section_type(section: WikitextContentNode) -> CardType | None:
    type_nodes = list(filter(lambda x: x.name == 'Wortart', section.children))
    if not type_nodes:
        return None
    assert len(type_nodes) == 1

    match type_nodes[0].plain_args[0]:
        case 'Substantiv':
            return CardType.Noun
    return None


def _maybe_extract_definitions(wiki_tree_node: WikitextContentNode, wiki_title: str,
                               target_translation_language_codes: List[str]) -> List[WiktionaryWordDefinition]:
    type_found = _maybe_get_section_type(wiki_tree_node)
    if type_found is None:
        nested_results = []
        for child_node in wiki_tree_node.children:
            nested_results += _maybe_extract_definitions(child_node, wiki_title, target_translation_language_codes)
        return nested_results

    result_definition = WiktionaryWordDefinition(wiki_title, type_found)
    result_definition.translations = _maybe_get_translations(wiki_tree_node, target_translation_language_codes)
    return [result_definition]


class GermanLocaleParser(WiktionaryLocalizedParser):
    @classmethod
    def translation_language_codes(cls) -> List[str]:
        return ['de']

    @classmethod
    def search_for_definitions(cls, search_text: str, target_translation_language_codes: List[str]) \
            -> StatusOr[List[WiktionaryWordDefinition]]:
        structured_articles_status = fetch_and_parse_matching_articles(search_text, locale='de')
        if not structured_articles_status.is_ok():
            return structured_articles_status.to_other()

        definitions_per_article = [
            _maybe_extract_definitions(article, article.name, target_translation_language_codes)
            for article in structured_articles_status.value
        ]
        results = itertools.chain(*definitions_per_article)
        return StatusOr(value=list(results))

    @classmethod
    # TODO: Comment
    def fetch_definitions(cls, titles: List[str]) -> StatusOr[List[WiktionaryWordDefinition]]:
        structured_articles_status = fetch_and_parse_articles(titles, locale='de')
        if not structured_articles_status.is_ok():
            return structured_articles_status.to_other()

        definitions_per_article = [
            _maybe_extract_definitions(article, article.name, target_translation_language_codes=[])
            for article in structured_articles_status.value
        ]
        results = itertools.chain(*definitions_per_article)
        return StatusOr(value=list(results))
