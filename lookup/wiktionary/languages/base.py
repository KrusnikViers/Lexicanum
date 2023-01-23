from typing import List, Dict

from core.types import CardType
from lookup.wiktionary.internal.markup import MarkupTreeNode


class WiktionaryTranslations:
    def __init__(self):
        self.meaning_note: str | None = None
        # Mapping {Language code: List of translations}
        self.translations: Dict[str, List[str]] = {}

    def __str__(self):
        if not self.translations:
            return ''
        translations_str = '\n'.join(['  - {} = {}'.format(x, ', '.join(y)) for x, y in self.translations.items()])
        return '\n  note: {}:\n{}'.format(self.meaning_note, translations_str)


class WiktionaryWordDefinition:
    def __init__(self, title: str, card_type: CardType):
        # Raw title of source wiktionary article.
        self.wiki_title = title
        # Short human-readable title, that could be used in answers.
        self.short_text = title
        # Full human-readable title with grammar information, that could be used in questions.
        self.grammar_text = title
        # Meaning note from the original article.
        self.meaning_note = ""

        self.card_type = card_type
        self.translations: List[WiktionaryTranslations] = []

    def __str__(self):
        return '{}:{}{}'.format(self.wiki_title, self.card_type.display_name(),
                                ''.join(map(str, self.translations)))


class WiktionaryLocalizedParser:
    @classmethod
    # Language code to access Wiktionary localized endpoint.
    def endpoint_language_code(cls) -> str:
        raise NotImplementedError

    @classmethod
    # Used for extracting translations from the wiki page. Multiple language codes can be suitable (e.g, 'high' and
    # 'simple' version of the same language).
    def translation_language_codes(cls) -> List[str]:
        raise NotImplementedError

    @classmethod
    # Returns list of different word definitions from the page. There could be multiple if word means multiple parts of
    # speech or have multiple meanings. Translations only filled for target translation language codes.
    def extract_word_definitions(
            cls, markup_tree: MarkupTreeNode, wiki_title: str, target_parser) -> List[WiktionaryWordDefinition]:
        raise NotImplementedError
