from typing import List, Dict

from core.types import CardType
from core.util import StatusOr


class WiktionaryTranslations:
    def __init__(self):
        self.meaning_note: str | None = None
        # Key: Language code
        # Value: List of translations
        self.translations: Dict[str, List[str]] = {}

    def __str__(self):
        translations_str = '\n'.join(['{} = {}'.format(x, ', '.join(y)) for x, y in self.translations.items()])
        return '---\n{}:\n{}'.format(self.meaning_note, translations_str)


class WiktionaryWordDefinition:
    def __init__(self, title: str, card_type: CardType):
        # Raw title of source wiktionary article
        self.wiki_title = title
        # Short human-readable title, that could be used in answers
        self.short_title = title
        # Full human-readable title with grammar information, that could be used in questions.
        self.grammar_string = title

        self.card_type = card_type
        self.translations: List[WiktionaryTranslations] = []

    def __str__(self):
        return '{}:{}\n{}'.format(self.wiki_title, self.card_type.display_name(),
                                  '\n'.join(map(str, self.translations)))


class WiktionaryLocalizedParser:
    @classmethod
    # Used to get translations from the corresponding wiki page section. For our purposes, multiple language codes can
    # be suitable (e.g, 'high' and 'simple' version of the same language).
    def translation_language_codes(cls) -> List[str]:
        raise NotImplementedError

    @classmethod
    # Get articles relevant to the |search_text|. Target translation codes are provided by the target parser, and only
    # relevant translations are kept.
    def search_for_definitions(cls, search_text: str, target_translation_language_codes: List[str]) \
            -> StatusOr[List[WiktionaryWordDefinition]]:
        raise NotImplementedError

    @classmethod
    # TODO: Comment
    def fetch_definitions(cls, titles: List[str]) -> StatusOr[List[WiktionaryWordDefinition]]:
        raise NotImplementedError
