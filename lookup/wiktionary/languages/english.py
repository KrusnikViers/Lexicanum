import itertools
from typing import List, Dict

from lookup.wiktionary.internal.markup_tree import MarkupTreeNode
from lookup.wiktionary.languages.base import WordDefinition, LocalizedParser, PartOfSpeech
from lookup.wiktionary.languages.utils import merge_translation_dict, all_children_recursive


def _get_word_forms(markup_node: MarkupTreeNode, wiki_title: str, node_type: PartOfSpeech) -> (str, str):
    as_answer = wiki_title.capitalize()
    if node_type == PartOfSpeech.Verb:
        as_answer = 'To {}'.format(wiki_title)
    as_question = as_answer
    return as_answer, as_question


def _get_meaning_note(markup_node: MarkupTreeNode) -> str:
    # TODO
    return ''


def _get_translations(markup_node: MarkupTreeNode, translation_codes: List[str]) -> List[str]:
    # language_code => translations list
    raw_results: Dict[str, List[str]] = dict()
    for child_node in all_children_recursive(markup_node):
        if child_node.name in ('t', 't+'):
            if len(child_node.plain_args) < 2:
                print('WTF')
                continue
            language = child_node.plain_args[0]
            translated_word = child_node.plain_args[1]
            if language in translation_codes and translated_word:
                raw_results.setdefault(language, []).append(translated_word)
    return list(itertools.chain(*merge_translation_dict(raw_results, translation_codes)))


_PART_OF_SPEECH_MAPPING = {
    'en-noun': PartOfSpeech.Noun,
    'en-verb': PartOfSpeech.Verb,
    'en-adj': PartOfSpeech.Adjective,
    'en-adv': PartOfSpeech.Adverb,
}


def _extract_word_definitions_recursive(markup_node: MarkupTreeNode,
                                        wiki_title: str, translation_codes: List[str]) -> List[WordDefinition]:
    node_types = [_PART_OF_SPEECH_MAPPING[node.name]
                  for node in markup_node.children if node.name in _PART_OF_SPEECH_MAPPING]

    if not node_types:
        nested_results = [_extract_word_definitions_recursive(child_node, wiki_title, translation_codes)
                          for child_node in markup_node.children]
        return list(itertools.chain(*nested_results))

    results = []
    for node_type in node_types:
        word_as_answer, word_as_question = _get_word_forms(markup_node, wiki_title, node_type)
        meaning_note = _get_meaning_note(markup_node)
        translations = _get_translations(markup_node, translation_codes)
        results.append(WordDefinition(part_of_speech=node_type, wiki_title=wiki_title,
                                      word_as_answer=word_as_answer, word_as_question=word_as_question,
                                      meaning_note=meaning_note,
                                      translation_wiki_titles=translations))
    return results


class EnglishLocaleParser(LocalizedParser):
    @classmethod
    def api_language_code(cls) -> str:
        return 'en'

    @classmethod
    def language_codes_for_translations(cls) -> List[str]:
        return ['en']

    @classmethod
    def extract_word_definitions(cls, markup_tree: MarkupTreeNode, wiki_title: str,
                                 language_codes_for_translations: List[str]) -> List[WordDefinition]:
        # debug.maybe_print_en_wikitree(markup_tree)
        return _extract_word_definitions_recursive(markup_tree, wiki_title, language_codes_for_translations)
