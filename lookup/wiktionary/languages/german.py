import itertools
from typing import List, Dict

from lookup.wiktionary.internal.markup_tree import MarkupTreeNode
from lookup.wiktionary.languages.base import WordDefinition, LocalizedParser, PartOfSpeech
from lookup.wiktionary.languages.utils import merge_translation_dict, all_children_recursive


def _get_noun_word_forms(markup_node: MarkupTreeNode) -> (str, str):
    _ARTICLES = {'n': 'Das', 'm': 'Der', 'f': 'Die'}
    article = None
    singular_form = None
    plural_form = None

    sections_to_check = [markup_node] + markup_node.children
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
        return singular_form, '{} / {}'.format(singular_form, plural_form)
    elif singular_form:
        return singular_form, '{} / nur Sing.'.format(singular_form)
    elif plural_form:
        return plural_form, '{} / nur Plur.'.format(plural_form)


def _get_word_forms(markup_node: MarkupTreeNode, wiki_title: str, node_type: PartOfSpeech) -> (str, str):
    match node_type:
        case PartOfSpeech.Noun:
            return _get_noun_word_forms(markup_node)
        case _:
            return wiki_title.capitalize(), wiki_title.capitalize()


def _get_meaning_note(markup_node: MarkupTreeNode) -> str:
    # TODO
    return ''


def _get_translations(markup_node: MarkupTreeNode, translation_codes: List[str]) -> List[str]:
    # language_code => translations list
    raw_results: Dict[str, List[str]] = dict()
    for child_node in all_children_recursive(markup_node):
        if child_node.name in ('Ü', 'Üxx4', 'Üt'):
            if len(child_node.plain_args) < 2:
                continue
            language = child_node.plain_args[0]
            translated_word = child_node.plain_args[1]
            if language in translation_codes and translated_word:
                raw_results.setdefault(language, []).append(translated_word)
    return list(itertools.chain(*merge_translation_dict(raw_results, translation_codes)))


_PART_OF_SPEECH_MAPPING = {
    'Substantiv': PartOfSpeech.Noun,
    'Verb': PartOfSpeech.Verb,
    'Adjektiv': PartOfSpeech.Adjective,
    'Adverb': PartOfSpeech.Adverb,
}


def _extract_word_definitions_recursive(markup_node: MarkupTreeNode,
                                        wiki_title: str, translation_codes: List[str]) -> List[WordDefinition]:
    node_types = [_PART_OF_SPEECH_MAPPING[node.plain_args[0]]
                  for node in markup_node.children
                  if node.name == 'Wortart' and node.plain_args[0] in _PART_OF_SPEECH_MAPPING]

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


class GermanLocaleParser(LocalizedParser):
    @classmethod
    def api_language_code(cls) -> str:
        return 'de'

    @classmethod
    def language_codes_for_translations(cls) -> List[str]:
        return ['de']

    @classmethod
    def extract_word_definitions(cls, markup_tree: MarkupTreeNode, wiki_title: str,
                                 language_codes_for_translations: List[str]) -> List[WordDefinition]:
        # debug.maybe_print_de_wikitree(markup_tree)
        return _extract_word_definitions_recursive(markup_tree, wiki_title, language_codes_for_translations)
