from typing import NamedTuple, List

from core.types.card_type import CardType

# CardTypes should cover all the parts of speech we're going to extract, so we will be using this enumeration to prevent
# possible divergence.
PartOfSpeech = CardType


class Definition(NamedTuple):
    part_of_speech: PartOfSpeech

    # Raw title of source wiktionary article. Do not alter, to allow fetching original article with this value.
    raw_article_title: str
    # Short human-readable string, well describing main form of the word. Can be used as question or an answer.
    readable_name: str
    # Additional grammar information (most often, non-standard word forms). Used to complement the question.
    grammar_note: str
    # Short note to identify meaning when only question is visible.
    meaning_note: str
    # Titles of articles with translations.
    translation_articles: List[str]

    def __str__(self):
        return '{} {} (raw {}/gram {}/mean {}/tr {})'.format(self.readable_name, self.part_of_speech.name,
                                                             self.raw_article_title,
                                                             self.grammar_note, self.meaning_note,
                                                             ','.join(self.translation_articles))
