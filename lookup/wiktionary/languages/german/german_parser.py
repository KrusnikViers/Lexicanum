from typing import List

from lookup.wiktionary.languages.base import *
from lookup.wiktionary.types import PartOfSpeech, MarkupTree, DefinitionComponent, DCType, DCTranslation

_PART_OF_SPEECH_MAPPING = {
    'Substantiv': PartOfSpeech.Noun,
    'Toponym': PartOfSpeech.Noun,
    'Verb': PartOfSpeech.Verb,
    'Adjektiv': PartOfSpeech.Adjective,
    'Gradpartikel': PartOfSpeech.Adverb,
    'Redewendung': PartOfSpeech.Phrase,
    'Wortverbindung': PartOfSpeech.Phrase,
}


def _is_proper_descriptor_node(node: MarkupTree) -> bool:
    return node.name == 'Wortart' and \
           len(node.plain_args) == 2 and \
           node.plain_args[0] in _PART_OF_SPEECH_MAPPING and \
           node.plain_args[1] in ('Deutsch')


def _grammar_components(node: MarkupTree) -> List[DefinitionComponent]:
    name_parts = node.name.split()
    if len(name_parts) != 3 or name_parts[1] not in _PART_OF_SPEECH_MAPPING:
        return []

    match _PART_OF_SPEECH_MAPPING[name_parts[1]]:
        case PartOfSpeech.Noun:
            genus = node.keyed_args.get('Genus', 'n')
            gendered_article = {'n': 'Das', 'm': 'Der', 'f': 'Die'}[genus]

            singular_key = 'Nominativ Singular'
            singular_form = '{} {}'.format(gendered_article, node.keyed_args[singular_key]) \
                if singular_key in node.keyed_args and node.keyed_args[singular_key] not in (' ', '-' '—') else None
            plural_key = 'Nominativ Plural'
            plural_form = 'Die {}'.format(node.keyed_args[plural_key]) \
                if plural_key in node.keyed_args and node.keyed_args[plural_key] not in (' ', '-', '—') else None
            if not singular_form and not plural_form:
                return []

            readable_form = singular_form if singular_form else plural_form
            grammar_note = plural_form if singular_form and plural_form else \
                'Nur singular' if singular_form else 'Nur plural'
            return [
                DefinitionComponent(node.level, DCType.ReadableForm, readable_form),
                DefinitionComponent(node.level, DCType.GrammarNote, grammar_note),
            ]
    return []


def _part_of_speech_components(node: MarkupTree, wiki_title: str) -> List[DefinitionComponent]:
    pos_dc = DefinitionComponent(node.level, DCType.PartOfSpeech, _PART_OF_SPEECH_MAPPING[node.plain_args[0]])
    result = [pos_dc]
    # Construct fallback readable form, if no explicit grammar information provided.
    readable_form = wiki_title.replace('_', ' ')
    if pos_dc.value in (PartOfSpeech.Noun, PartOfSpeech.Phrase):
        result.append(DefinitionComponent(node.level + 1, DCType.ReadableForm, readable_form.capitalize()))
    else:
        result.append(DefinitionComponent(node.level + 1, DCType.ReadableForm, readable_form.lower()))
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
            if _is_proper_descriptor_node(node):
                result += _part_of_speech_components(node, source_wiki_title)
            elif node.name.endswith('Übersicht'):
                result += _grammar_components(node)
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
