import itertools
from typing import List, Tuple

from lookup.wiktionary.languages import LocalizedParser
from lookup.wiktionary.types import MarkupTree, Definition, PartOfSpeech


def _try_get_noun_word_forms(markup_node: MarkupTree) -> Tuple[str, str] | None:
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
        return singular_form, plural_form
    elif singular_form:
        return singular_form, 'nur Singular.'
    elif plural_form:
        return plural_form, 'nur Plural'
    else:
        return None


def _try_get_word_forms(markup_node: MarkupTree,
                        wiki_title: str,
                        node_type: PartOfSpeech) -> Tuple[str, str] | None:
    match node_type:
        case PartOfSpeech.Noun:
            return _try_get_noun_word_forms(markup_node)
        case _:
            return wiki_title.capitalize(), ''


def _get_meaning_note(markup_node: MarkupTree) -> str:
    # TODO
    return ''


def _get_translations(markup_node: MarkupTree, translation_codes: List[str]) -> List[str]:
    # language_code => translations list
    raw_results = []
    for child_node in markup_node.children_recursive():
        if child_node.name in ('Ü', 'Üxx4', 'Üt'):
            if len(child_node.plain_args) < 2:
                continue
            language = child_node.plain_args[0]
            translated_word = child_node.plain_args[1]
            if language in translation_codes and translated_word:
                raw_results.append(translated_word)
    return raw_results


_PART_OF_SPEECH_MAPPING = {
    'Substantiv': PartOfSpeech.Noun,
    'Verb': PartOfSpeech.Verb,
    'Adjektiv': PartOfSpeech.Adjective,
    'Adverb': PartOfSpeech.Adverb,
}


def _extract_word_definitions_recursive(markup_node: MarkupTree,
                                        wiki_title: str, translation_codes: List[str]) -> List[Definition]:
    node_types = [_PART_OF_SPEECH_MAPPING[node.plain_args[0]]
                  for node in markup_node.children
                  if node.name == 'Wortart' and node.plain_args[0] in _PART_OF_SPEECH_MAPPING]

    if not node_types:
        nested_results = [_extract_word_definitions_recursive(child_node, wiki_title, translation_codes)
                          for child_node in markup_node.children]
        return list(itertools.chain(*nested_results))

    results = []
    for node_type in node_types:
        forms = _try_get_word_forms(markup_node, wiki_title, node_type)
        if forms is None:
            continue
        word_readable, grammar_forms = forms
        meaning_note = _get_meaning_note(markup_node)
        translations = _get_translations(markup_node, translation_codes)
        results.append(Definition(part_of_speech=node_type, raw_article_title=wiki_title,
                                  readable_name=word_readable, grammar_note=grammar_forms,
                                  meaning_note=meaning_note,
                                  translation_articles=translations))
    return results


class GermanLocaleParser(LocalizedParser):
    @classmethod
    def api_language_code(cls) -> str:
        return 'de'

    @classmethod
    def language_codes_for_translations(cls) -> List[str]:
        return ['de']

    @classmethod
    def extract_word_definitions(cls, markup_tree: MarkupTree, wiki_title: str,
                                 language_codes_for_translations: List[str]) -> List[Definition]:
        # debug.maybe_print_de_wikitree(markup_tree)
        return _extract_word_definitions_recursive(markup_tree, wiki_title, language_codes_for_translations)
