from typing import List

from lookup.wiktionary.languages.base import *
from lookup.wiktionary.types import PartOfSpeech, MarkupTree, DefinitionComponent, DCType, DCTranslation

_PART_OF_SPEECH_MAPPING = {
    'en-noun': PartOfSpeech.Noun,
    'en-proper noun': PartOfSpeech.Noun,
    'en-plural noun': PartOfSpeech.Noun,
    'en-verb': PartOfSpeech.Verb,
    'en-adj': PartOfSpeech.Adjective,
    'en-adv': PartOfSpeech.Adverb,
}


def _part_of_speech_components(node: MarkupTree, wiki_title: str) -> List[DefinitionComponent]:
    pos_dc = DefinitionComponent(node.level, DCType.PartOfSpeech, _PART_OF_SPEECH_MAPPING[node.name])
    result = [pos_dc]
    if pos_dc.value == PartOfSpeech.Verb:
        result.append(
            DefinitionComponent(node.level, DCType.ReadableForm, 'to {}'.format(wiki_title)))
    elif pos_dc.value in (PartOfSpeech.Noun,):
        result.append(DefinitionComponent(node.level, DCType.ReadableForm, wiki_title.capitalize()))
    else:
        result.append(DefinitionComponent(node.level, DCType.ReadableForm, wiki_title.lower()))
    return result


def _translation_components(node: MarkupTree, language_codes_for_translations: List[str]) -> List[DefinitionComponent]:
    if len(node.plain_args) > 1 and node.plain_args[0] in language_codes_for_translations and node.plain_args[1]:
        return [DefinitionComponent(node.level, DCType.Translation,
                                    DCTranslation(lang=node.plain_args[0], text=node.plain_args[1]))]
    return []


class EnglishLocaleParser(LocalizedParser):
    @classmethod
    def extract_definition_components(cls, markup_tree: MarkupTree, source_wiki_title: str,
                                      language_codes_for_translations: List[str]) -> List[DefinitionComponent]:
        result = []
        for node in markup_tree.children:
            if node.name.startswith('en-'):
                result += [DefinitionComponent(node.level, DCType.Separator)]
            if node.name in _PART_OF_SPEECH_MAPPING:
                result += _part_of_speech_components(node, source_wiki_title)
            elif node.name in ('t', 'tt', 't+', 'tt+'):
                result += _translation_components(node, language_codes_for_translations)
            result += cls.extract_definition_components(node, source_wiki_title, language_codes_for_translations)
        return result

    @classmethod
    def api_language_code(cls) -> str:
        return 'en'

    @classmethod
    def language_codes_for_translations(cls) -> List[str]:
        return ['en']
