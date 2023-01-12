from typing import List

from core.types import CardType
from lookup.wiktionary.debug import *
from lookup.wiktionary.internal.markup import WikitextContentNode
from lookup.wiktionary.languages.base import WiktionaryWordDefinition, WiktionaryTranslations, WiktionaryLocalizedParser


def _fill_translations(section: WikitextContentNode, target_translation_language_codes: List[str],
                       definition: WiktionaryWordDefinition):
    raw_results = []
    for node in section.children:
        if node.name == 'trans-top':
            new_node = WiktionaryTranslations()
            if node.plain_args:
                new_node.meaning_note = node.plain_args[0]
            raw_results.append(new_node)
        if node.name in ('t', 't+') and node.plain_args[0] in target_translation_language_codes:
            if not len(raw_results):
                raw_results.append(WiktionaryTranslations())
            language_code = node.plain_args[0]
            translations = raw_results[-1].translations
            if language_code not in translations:
                translations[language_code] = [node.plain_args[1]]
            else:
                translations[language_code].append(node.plain_args[1])
    definition.translations += [translation for translation in raw_results if len(translation.translations)]
    for child_node in section.children:
        _fill_translations(child_node, target_translation_language_codes, definition)


def _maybe_get_section_types(section: WikitextContentNode) -> [CardType]:
    _MAPPING = {
        'en-noun': CardType.Noun,
        'en-verb': CardType.Verb,
        'en-adj': CardType.Adjective,
        'en-adv': CardType.Adverb,
    }
    return [_MAPPING[node.name] for node in section.children if node.name in _MAPPING]


def _fill_word_forms(section: WikitextContentNode, word_type: CardType, definition: WiktionaryWordDefinition):
    if word_type == CardType.Verb:
        definition.short_title = 'To {}'.format(definition.wiki_title)
    else:
        definition.short_title = definition.wiki_title.capitalize()
    definition.grammar_string = definition.short_title


class EnglishLocaleParser(WiktionaryLocalizedParser):
    @classmethod
    def endpoint_language_code(cls) -> str:
        return 'en'

    @classmethod
    def translation_language_codes(cls) -> List[str]:
        return ['en']

    @classmethod
    def extract_word_definitions(cls, wiki_tree_node: WikitextContentNode, wiki_title: str,
                                 target_translation_language_codes: List[str]) -> List[WiktionaryWordDefinition]:
        if wiki_tree_node.level == -1 and PRINT_WIKITREE_EN:
            print('======Extracting DE definition {} >>'.format(wiki_title))
            print(wiki_tree_node)
            print('======Extracting DE definition {} <<'.format(wiki_title))

        types_found = _maybe_get_section_types(wiki_tree_node)
        if not types_found:
            nested_results = []
            for child_node in wiki_tree_node.children:
                nested_results += cls.extract_word_definitions(child_node, wiki_title,
                                                               target_translation_language_codes)
            return nested_results

        result = []
        for type_found in types_found:
            new_definition = WiktionaryWordDefinition(wiki_title, type_found)
            _fill_word_forms(wiki_tree_node, type_found, new_definition)
            _fill_translations(wiki_tree_node, target_translation_language_codes, new_definition)
            result.append(new_definition)
        return result
