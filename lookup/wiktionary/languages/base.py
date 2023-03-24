from typing import List, NamedTuple

from core.types import CardType
from lookup.wiktionary.internal.markup_tree import MarkupTreeNode


class Translations(NamedTuple):
    # Filled only by 'answers' parsers
    meaning_note: str = ''
    # Raw versions of translation words (thus suitable for looking up as wiktionary articles)
    words: List[str] = []


class WordDefinition(NamedTuple):
    card_type: CardType
    # Raw title of source wiktionary article.
    wiki_title: str
    # Short human-readable string
    word_as_answer: str
    # Full human-readable form with grammar information (e.g. additional forms)
    word_as_question: str
    # Short note to identify meaning when only question is visible. Must be given in the same language as answer.
    meaning_note: str
    translations: Translations


class LocalizedParser:
    @classmethod
    # Language code to access Wiktionary localized endpoint.
    def language_code(cls) -> str:
        raise NotImplementedError

    @classmethod
    # Used for extracting translations from the wiki page. Usually just main language code, but multiple language codes
    # can be suitable as well (e.g. 'high' and 'common' version of the same language).
    def language_codes_for_translations(cls) -> List[str]:
        raise NotImplementedError

    @classmethod
    # Returns list of different word definitions from the page. There could be multiple if word means multiple parts of
    # speech or have multiple meanings. Translations only filled for target translation language codes.
    def extract_word_definitions(cls, markup_tree: MarkupTreeNode, source_wiki_title: str,
                                 language_codes_for_translations: List[str]) -> List[WordDefinition]:
        raise NotImplementedError
