import re
from typing import List

from core.util import safe_get
from lookup.wiktionary.languages.base import *
from lookup.wiktionary.languages.english.grammar_components import grammar_components
from lookup.wiktionary.languages.english.shared_constants import *
from lookup.wiktionary.types import MarkupTree, DefinitionComponent, DCType, DCTranslation


# Returns None only if node is not word definition key. If part of speech can not be identified, returns empty string.
def _maybe_get_poskey(node: MarkupTree) -> str | None:
    # Value reserved for verb conjugations
    if node.name == 'en-conj':
        return None
    if not node.name.startswith(POS_KEY_PREFIX) and node.name != POS_KEY_FULL:
        return None
    if node.name.startswith(POS_KEY_PREFIX):
        return node.name[len(POS_KEY_PREFIX):]
    elif node.name == POS_KEY_FULL and \
            safe_get(node.plain_args, 0) in ('en',) and \
            safe_get(node.plain_args, 1):
        return node.plain_args[1]
    return str()


def _pos_and_grammar_components(node: MarkupTree, wiki_title: str) -> List[DefinitionComponent]:
    pos = _maybe_get_poskey(node)
    if pos not in POS_MAP:
        return []
    pos_dc = DefinitionComponent(node.level, DCType.PartOfSpeech, POS_MAP[pos])
    result = [pos_dc]

    # Construct fallback readable form, if no explicit grammar information provided.
    readable_form = wiki_title.replace('_', ' ')
    result.append(DefinitionComponent(node.level + 1, DCType.ReadableForm, readable_form.capitalize()))
    result += grammar_components(node, POS_MAP[pos], wiki_title)

    return result


def _translation_components(node: MarkupTree, language_codes_for_translations: List[str]) -> List[DefinitionComponent]:
    if safe_get(node.plain_args, 0) in language_codes_for_translations and safe_get(node.plain_args, 1):
        translation_text = node.plain_args[1]
        if '[[' in translation_text:
            links = re.findall('\\[\\[.*?]]', translation_text)
            if not links:
                return []
            translation_text = ' '.join([link[2:-2] for link in links]).strip()
        if not translation_text:
            return []
        return [DefinitionComponent(node.level, DCType.Translation,
                                    DCTranslation(lang=node.plain_args[0], text=translation_text))]
    return []


class EnglishLocaleParser(LocalizedParser):
    @classmethod
    def extract_definition_components(cls, markup_tree: MarkupTree, source_wiki_title: str,
                                      language_codes_for_translations: List[str]) -> List[DefinitionComponent]:
        result = []
        for node in markup_tree.children:
            if _maybe_get_poskey(node) is not None:
                result += [DefinitionComponent(node.level, DCType.Separator)]
                result += _pos_and_grammar_components(node, source_wiki_title)
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
