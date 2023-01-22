from typing import List

from core.types import CardType
from lookup.wiktionary.debug import *
from lookup.wiktionary.internal.markup import WikitextContentNode
from lookup.wiktionary.languages.base import WiktionaryWordDefinition, WiktionaryTranslations, WiktionaryLocalizedParser


def _fill_translations(section: WikitextContentNode, target_translation_language_codes: List[str],
                       definition: WiktionaryWordDefinition):
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
    definition.translations += meaningful_results
    for child_node in section.children:
        _fill_translations(child_node, target_translation_language_codes, definition)


def _fill_noun_word_forms(section: WikitextContentNode, definition: WiktionaryWordDefinition):
    _ARTICLES = {'n': 'Das', 'm': 'Der', 'f': 'Die'}
    article = None
    singular_form = None
    plural_form = None

    sections_to_check = [section] + section.children
    for section in sections_to_check:
        for key, value in section.keyed_args.items():
            if key == 'Genus' and value in _ARTICLES and not article:
                article = _ARTICLES[value]
            elif key.startswith('Nominativ Singular') and not singular_form and value != '—':
                singular_form = value
            elif key.startswith('Nominativ Plural') and not plural_form and value != '—':
                plural_form = value

    singular_form = '{} {}'.format(article, singular_form) if article and singular_form else None
    plural_form = 'Die {}'.format(plural_form) if plural_form else None
    if singular_form and plural_form:
        definition.short_title = singular_form
        definition.grammar_string = '{} / {}'.format(singular_form, plural_form)
    elif singular_form:
        definition.short_title = singular_form
        definition.grammar_string = '{} / nur Sing.'.format(singular_form)
    elif plural_form:
        definition.short_title = plural_form
        definition.grammar_string = '{} / nur Plur.'.format(plural_form)


def _fill_word_forms(section: WikitextContentNode, definition: WiktionaryWordDefinition):
    definition.short_title = definition.wiki_title.capitalize()
    definition.grammar_string = definition.short_title
    if definition.card_type == CardType.Noun:
        _fill_noun_word_forms(section, definition)


def _maybe_get_section_types(section: WikitextContentNode) -> [CardType]:
    type_nodes = list(filter(lambda x: x.name == 'Wortart', section.children))
    if not type_nodes:
        return None
    _MAPPING = {
        'Substantiv': CardType.Noun,
        'Verb': CardType.Verb,
        'Adjektiv': CardType.Adjective,
        'Adverb': CardType.Adverb,
    }
    return [_MAPPING[node.plain_args[0]] for node in type_nodes if node.plain_args[0] in _MAPPING]


class GermanLocaleParser(WiktionaryLocalizedParser):
    @classmethod
    def endpoint_language_code(cls) -> str:
        return 'de'

    @classmethod
    def translation_language_codes(cls) -> List[str]:
        return ['de']

    @classmethod
    def extract_word_definitions(cls, wiki_tree_node: WikitextContentNode, wiki_title: str,
                                 target_translation_language_codes: List[str]) -> List[WiktionaryWordDefinition]:
        if wiki_tree_node.level == -1 and PRINT_WIKITREE_DE:
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
            _fill_translations(wiki_tree_node, target_translation_language_codes, new_definition)
            _fill_word_forms(wiki_tree_node, new_definition)
            result.append(new_definition)
        return result
