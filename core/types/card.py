from core.types.card_type import CardType

from core.util import Status


class Card:
    LINE_DELIMITER = ';'

    def __init__(self, card_type: CardType,
                 question: str, grammar_note: str, answer: str, meaning_note: str,
                 card_id: int | None = None):
        # Type of card. Can be part of speech or complex concept (e.g. whole phrase or grammar rule)
        self.card_type: CardType = card_type
        # Readable and the most common form of a word or a phrase in the language that is being learned.
        self.question: str = question
        # Additional grammar info (e.g. plural form, or additional word forms that do not follow usual rules).
        self.grammar_note: str = grammar_note
        # Readable and the most common form of a word or a phrase in the language already known.
        self.answer: str = answer
        # Additional information about the meaning in the language already known. Helps to disambiguate full homonyms.
        self.meaning_note: str = meaning_note
        # Internal Anki identifier. Helps to keep track of the card history even if the contents change.
        self.card_id: int | None = card_id

    def validity_status(self) -> Status:
        if not self.question.strip():
            return Status("Question field can not be empty")
        elif not self.answer.strip():
            return Status("Answer field can not be empty")
        elif self.card_type == CardType.Invalid:
            return Status("Choose card type")
        return Status()

    def __str__(self):
        return 'Card: {}=>{} {} (gram {}/mean {}/id {})'.format(self.question, self.answer, self.card_type.name,
                                                                self.grammar_note, self.meaning_note, self.card_id)

    def normalize_for_output(self):
        self.question = self.question.strip()
        self.answer = self.answer.strip()
        self.meaning_note = self.meaning_note.strip()

        grammar_note_lines = self.grammar_note.split(self.LINE_DELIMITER)
        normalized_delimiter = '{} '.format(self.LINE_DELIMITER)
        self.grammar_note = normalized_delimiter.join(line.strip() for line in grammar_note_lines)

    @classmethod
    def from_dict(cls, card_dict: dict) -> 'Card':
        return cls(CardType(card_dict['card_type']),
                   card_dict['question'],
                   card_dict['grammar_note'],
                   card_dict['answer'],
                   card_dict['meaning_note'],
                   card_dict['card_id'])

    def to_dict(self) -> dict:
        assert self.card_id is not None, "Missing deck normalization?"
        assert self.card_type is not CardType.Invalid
        return {'card_type': self.card_type.value,
                'question': self.question,
                'grammar_note': self.grammar_note,
                'answer': self.answer,
                'meaning_note': self.meaning_note,
                'card_id': self.card_id,
                }
