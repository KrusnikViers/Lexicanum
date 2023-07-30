import itertools
from typing import List

from lookup.wiktionary.languages.base import LocalizedParser, TranslationsListBuilder
from lookup.wiktionary.types import PartOfSpeech, MarkupTree, Definition


def _get_word_forms(markup_node: MarkupTree, wiki_title: str, node_type: PartOfSpeech) -> (str, str):
    as_answer = wiki_title.capitalize()
    if node_type == PartOfSpeech.Verb:
        as_answer = 'To {}'.format(wiki_title)
    as_question = as_answer
    return as_answer, as_question


def _get_meaning_note(markup_node: MarkupTree) -> str:
    # TODO
    return ''


def _get_translations(markup_node: MarkupTree, translation_codes: List[str]) -> List[str]:
    list_builder = TranslationsListBuilder(translation_codes)
    for child_node in markup_node.children_recursive():
        if child_node.name in ('t', 't+'):
            if len(child_node.plain_args) < 2:
                continue
            language = child_node.plain_args[0]
            translated_word = child_node.plain_args[1]
            if language in translation_codes and translated_word:
                list_builder.add(translated_word, language)
    return list_builder.result()


_PART_OF_SPEECH_MAPPING = {
    'en-noun': PartOfSpeech.Noun,
    'en-verb': PartOfSpeech.Verb,
    'en-adj': PartOfSpeech.Adjective,
    'en-adv': PartOfSpeech.Adverb,
}


def _extract_word_definitions_recursive(markup_node: MarkupTree,
                                        wiki_title: str, translation_codes: List[str]) -> List[Definition]:
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
        results.append(Definition(part_of_speech=node_type, raw_article_title=wiki_title,
                                  readable_name=word_as_answer, grammar_note=word_as_question,
                                  translation_articles=translations))
    return results


class EnglishLocaleParser(LocalizedParser):
    @classmethod
    def api_language_code(cls) -> str:
        return 'en'

    @classmethod
    def language_codes_for_translations(cls) -> List[str]:
        return ['en']

    @classmethod
    def extract_word_definitions(cls, markup_tree: MarkupTree, wiki_title: str,
                                 language_codes_for_translations: List[str]) -> List[Definition]:
        return _extract_word_definitions_recursive(markup_tree, wiki_title, language_codes_for_translations)
