from enum import Enum
from typing import List, NamedTuple, Any

from lookup.wiktionary.languages.base import *
from lookup.wiktionary.types import PartOfSpeech, MarkupTree, Definition

_PART_OF_SPEECH_MAPPING = {
    'en-noun': PartOfSpeech.Noun,
    'en-verb': PartOfSpeech.Verb,
    'en-adj': PartOfSpeech.Adjective,
    'en-adv': PartOfSpeech.Adverb,
}


class _DefinitionPart(NamedTuple):
    class Type(Enum):
        PartOfSpeech = 1
        ReadableForm = 2
        Translation = 3

    part_type: Type
    level: int
    value: Any

    def __str__(self):
        return '|' * self.level + '- {} : {}'.format(self.part_type.name, str(self.value))


def _node_children_to_parts(parent_node: MarkupTree, translation_languages: List[str]) -> List[_DefinitionPart]:
    result = []
    for node in parent_node.children:
        if node.name in _PART_OF_SPEECH_MAPPING:
            result.append(
                _DefinitionPart(_DefinitionPart.Type.PartOfSpeech, node.level, _PART_OF_SPEECH_MAPPING[node.name]))
        elif node.name in ('t', 't+'):
            if len(node.plain_args) > 1 and node.plain_args[0] in translation_languages:
                result.append(_DefinitionPart(
                    _DefinitionPart.Type.Translation, node.level, (node.plain_args[0], node.plain_args[1])))
        result += _node_children_to_parts(node, translation_languages)
    return result


def _part_of_speech_components(node: MarkupTree, wiki_title: str) -> List[DefinitionComponent]:
    pos_dc = PartOfSpeechDC(_PART_OF_SPEECH_MAPPING[node.name], node.level)
    if pos_dc.part_of_speech == PartOfSpeech.Verb:
        rdf_dc = ReadableFormDC('to {}'.format(wiki_title), node.level)
    elif pos_dc.part_of_speech in (PartOfSpeech.Noun,):
        rdf_dc = ReadableFormDC(wiki_title.capitalize(), node.level)
    else:
        rdf_dc = ReadableFormDC(wiki_title, node.level)
    return [pos_dc, rdf_dc]


def _translation_components(node: MarkupTree, language_codes_for_translations: List[str]) -> List[DefinitionComponent]:
    if len(node.plain_args) > 1 and node.plain_args[0] in language_codes_for_translations:
        return [TranslationDC(node.plain_args[0], node.plain_args[1], node.level)]
    return []


class EnglishLocaleParser(LocalizedParser):
    @classmethod
    def api_language_code(cls) -> str:
        return 'en'

    @classmethod
    def language_codes_for_translations(cls) -> List[str]:
        return ['en']

    @classmethod
    def extract_definition_components_from_markup(
            cls, markup_tree: MarkupTree, wiki_title: str,
            language_codes_for_translations: List[str]) -> List[DefinitionComponent]:
        result = []
        for node in markup_tree.children:
            if node.name in _PART_OF_SPEECH_MAPPING:
                result += _part_of_speech_components(node, wiki_title)
            elif node.name in ('t', 't+'):
                result += _translation_components(node, language_codes_for_translations)

            result += cls.extract_definition_components_from_markup(node, wiki_title, language_codes_for_translations)

        return result

    @classmethod
    def extract_word_definitions(cls, markup_tree: MarkupTree, wiki_title: str,
                                 language_codes_for_translations: List[str]) -> List[Definition]:
        parts = _node_children_to_parts(markup_tree, language_codes_for_translations)
        print('--- ' + wiki_title + ' ---')
        for part in parts:
            print(part)
        return []
