import itertools
from typing import List

from core.types import CardType
from core.util import StatusOr
from lookup.wiktionary.internal import WikitextTreeNode, fetch_structured_articles
from lookup.wiktionary.languages.base import WiktionaryWordDefinition, WiktionaryTranslations, WiktionaryLocalizedParser


def _normalize_title(title: str):
    return title


def _maybe_get_translations(section: WikitextTreeNode, target_translation_language_codes: List[str]) -> []:
    results = []
    for node in section.nodes:
        if node.name == 'trans-top':
            new_node = WiktionaryTranslations()
            if node.plain_args:
                new_node.meaning_note = node.plain_args[0]
            results.append(new_node)
        if node.name in ('t', 't+') and node.plain_args[0] in target_translation_language_codes:
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


def _maybe_get_section_type(section: WikitextTreeNode) -> CardType | None:
    for node in section.nodes:
        match node.name:
            case 'en-noun':
                return CardType.Noun
            case 'en-verb':
                return CardType.Verb
    return None


def _maybe_extract_definitions(wiki_tree_node: WikitextTreeNode, wiki_title: str,
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


class EnglishLocaleParser(WiktionaryLocalizedParser):
    @classmethod
    def translation_language_codes(cls) -> List[str]:
        return ['en']

    @classmethod
    def fetch_and_parse_word_definitions(cls, search_text: str, target_translation_language_codes: List[str]) \
            -> StatusOr[List[WiktionaryWordDefinition]]:
        structured_articles_status = fetch_structured_articles(search_text, locale='en')
        if not structured_articles_status.is_ok():
            return structured_articles_status.to_other()

        definitions_per_article = [
            _maybe_extract_definitions(article, article.title, target_translation_language_codes) for
            article in structured_articles_status.value
        ]
        results = itertools.chain(*definitions_per_article)
        for result in results:
            print(result)
        return StatusOr(status='Not implemented')
