from typing import List

from core.util import safe_get
from lookup.wiktionary.languages.base import *
from lookup.wiktionary.languages.german.grammar_components import grammar_components, pronoun_grammar_components
from lookup.wiktionary.languages.german.shared_constants import *
from lookup.wiktionary.types import MarkupTree, DefinitionComponent, DCType, DCTranslation


def _part_of_speech_components(node: MarkupTree, wiki_title: str) -> List[DefinitionComponent]:
    assert node.name == POS_KEY
    if safe_get(node.plain_args, 0) not in POS_MAP or \
            safe_get(node.plain_args, 1) not in ('Deutsch',):
        return []

    pos_dc = DefinitionComponent(node.level, DCType.PartOfSpeech, POS_MAP[node.plain_args[0]])
    result = [pos_dc]

    # Construct fallback readable form, if no explicit grammar information provided.
    readable_form = wiki_title.replace('_', ' ')
    result.append(DefinitionComponent(node.level + 1, DCType.ReadableForm, readable_form.capitalize()))

    return result


def _translation_components(node: MarkupTree, language_codes_for_translations: List[str]) -> List[DefinitionComponent]:
    if safe_get(node.plain_args, 0) not in language_codes_for_translations or not safe_get(node.plain_args, 1):
        return []
    return [DefinitionComponent(node.level, DCType.Translation,
                                DCTranslation(lang=node.plain_args[0], text=node.plain_args[1]))]


class GermanLocaleParser(LocalizedParser):
    @classmethod
    def extract_definition_components(cls, markup_tree: MarkupTree, source_wiki_title: str,
                                      language_codes_for_translations: List[str]) -> List[DefinitionComponent]:
        result = []
        for node in markup_tree.children:
            if node.name == POS_KEY:
                result += [DefinitionComponent(node.level, DCType.Separator)]
                result += _part_of_speech_components(node, source_wiki_title)
            elif node.name.endswith('Übersicht'):
                result += grammar_components(node, source_wiki_title)
            elif node.name == 'Pronomina-Tabelle':
                result += pronoun_grammar_components(node)
            elif node.name in ('Üt', 'Ü', 'Ü?'):
                result += _translation_components(node, language_codes_for_translations)

            result += cls.extract_definition_components(node, source_wiki_title, language_codes_for_translations)

        return result

    @classmethod
    def api_language_code(cls) -> str:
        return 'de'

    @classmethod
    def language_codes_for_translations(cls) -> List[str]:
        return ['de']
