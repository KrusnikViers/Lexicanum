from typing import List, NamedTuple

from core.types import CardType
from lookup.wiktionary.internal.markup_tree import MarkupTreeNode

# CardTypes should cover all the parts of speech we're going to extract, so we will be using this enumeration to prevent
# possible divergence.
PartOfSpeech = CardType


class WordDefinition(NamedTuple):
    part_of_speech: PartOfSpeech

    # Raw title of source wiktionary article.
    wiki_title: str
    # Short human-readable string, well describing main form of the word
    word_readable: str
    # Additional grammar information (most likely, unusual word forms)
    grammar_note: str
    # Short note to identify meaning when only question is visible.

    meaning_note: str
    translation_wiki_titles: List[str]

    def __str__(self):
        return '{}, {}: {} ({}), meaning: {}, translations: {})'.format(self.wiki_title, self.part_of_speech.name,
                                                                        self.word_readable, self.grammar_note,
                                                                        self.meaning_note,
                                                                        ';'.join(self.translation_wiki_titles))


class LocalizedParser:
    @classmethod
    # Language code to access Wiktionary localized endpoint.
    def api_language_code(cls) -> str:
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
