from typing import List

from lookup.wiktionary.languages.base import *
from lookup.wiktionary.types import PartOfSpeech, MarkupTree, DefinitionComponent, DCType, DCTranslation

_PART_OF_SPEECH_MAPPING = {
    'Substantiv': PartOfSpeech.Noun,
    'Toponym': PartOfSpeech.Noun,
    'Verb': PartOfSpeech.Verb,
    'Adjektiv': PartOfSpeech.Adjective,
    'Gradpartikel': PartOfSpeech.Adverb
}


def _part_of_speech_components(node: MarkupTree, wiki_title: str) -> List[DefinitionComponent]:
    if node.name != 'Wortart' or len(node.plain_args) == 0 or node.plain_args[0] not in _PART_OF_SPEECH_MAPPING:
        return []
    pos_dc = DefinitionComponent(node.level, DCType.PartOfSpeech, _PART_OF_SPEECH_MAPPING[node.plain_args[0]])
    result = [pos_dc]
    if pos_dc.value in (PartOfSpeech.Noun,):
        result.append(DefinitionComponent(node.level, DCType.ReadableForm, wiki_title.capitalize()))
    else:
        result.append(DefinitionComponent(node.level, DCType.ReadableForm, wiki_title.lower()))
    return result


def _translation_components(node: MarkupTree, language_codes_for_translations: List[str]) -> List[DefinitionComponent]:
    if len(node.plain_args) > 1 and node.plain_args[0] in language_codes_for_translations and node.plain_args[1]:
        return [DefinitionComponent(node.level, DCType.Translation,
                                    DCTranslation(lang=node.plain_args[0], text=node.plain_args[1]))]
    return []


class GermanLocaleParser(LocalizedParser):
    @classmethod
    def extract_definition_components(cls, markup_tree: MarkupTree, source_wiki_title: str,
                                      language_codes_for_translations: List[str]) -> List[DefinitionComponent]:
        result = []
        for node in markup_tree.children:
            if node.name == 'Wortart':
                result += [DefinitionComponent(node.level, DCType.Separator)]
            if node.name == 'Wortart':
                result += _part_of_speech_components(node, source_wiki_title)
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
