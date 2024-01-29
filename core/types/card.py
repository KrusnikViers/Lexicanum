from core.types.card_type import CardType

from core.util import Status


class Card:
    LINE_DELIMITER = ';'

    def __init__(self, card_type: CardType,
                 question_main: str, question_grammar: str, question_ipa: str, question_example: str,
                 answer_main: str, answer_example: str, note: str, card_id: int | None = None):
        # Type of card. Can be part of speech or complex concept (e.g. whole phrase or grammar rule)
        self.card_type: CardType = card_type

        # Readable and the most common form of a word or a phrase in the language that is being learned.
        self.question_main: str = question_main
        # Additional grammar info (e.g. plural form, or additional word forms that do not follow usual rules).
        self.question_grammar: str = question_grammar
        # IPA info about common pronunciation.
        self.question_ipa: str = question_ipa
        # Example of usage in question language.
        self.question_example: str = question_example

        # Readable and the most common form of a word or a phrase in the language already known.
        self.answer_main: str = answer_main
        # Example of usage in answer language.
        self.answer_example: str = answer_example

        # Additional information about the meaning in the language already known. Helps to disambiguate full homonyms.
        self.note: str = note

        # Internal Anki identifier. Helps to keep track of the card history even if the contents change.
        self.card_id: int | None = card_id

    def validity_status(self) -> Status:
        if not self.question_main.strip():
            return Status("Question field can not be empty")
        elif not self.answer_main.strip():
            return Status("Answer field can not be empty")
        elif self.card_type == CardType.Invalid:
            return Status("Card type should be selected")
        return Status()

    def __str__(self):
        # TODO: Update
        return 'Card: {}=>{} {} (gram {}/mean {}/id {})'.format(self.question_main, self.answer_main,
                                                                self.card_type.name,
                                                                self.question_grammar, self.note, self.card_id)

    @classmethod
    def _normalize_multiline(cls, original_line: str) -> str:
        normalized_delimiter = '{} '.format(cls.LINE_DELIMITER)
        return normalized_delimiter.join(line.strip() for line in original_line.split(cls.LINE_DELIMITER))

    def normalize_for_output(self):
        self.question_main = self._normalize_multiline(self.question_main)
        self.question_grammar = self._normalize_multiline(self.question_grammar)
        self.question_ipa = self.question_ipa.strip()
        self.question_example = self._normalize_multiline(self.question_example)
        self.answer_main = self._normalize_multiline(self.answer_main)
        self.answer_example = self._normalize_multiline(self.answer_example)
        self.note = self._normalize_multiline(self.note)

    @classmethod
    def from_dict(cls, card_dict: dict) -> 'Card':
        return cls(card_type=CardType(card_dict['card_type']),
                   question_main=card_dict['question_main'],
                   question_grammar=card_dict['question_grammar'],
                   question_ipa=card_dict['question_ipa'],
                   question_example=card_dict['question_example'],
                   answer_main=card_dict['answer_main'],
                   answer_example=card_dict['answer_example'],
                   note=card_dict['note'],
                   card_id=card_dict['card_id'])

    def to_dict(self) -> dict:
        assert self.card_id is not None, "Missing deck normalization?"
        assert self.card_type is not CardType.Invalid
        return {'card_type': self.card_type.value,
                'question_main': self.question_main,
                'question_grammar': self.question_grammar,
                'question_ipa': self.question_ipa,
                'question_example': self.question_example,
                'answer_main': self.answer_main,
                'answer_example': self.answer_example,
                'note': self.note,
                'card_id': self.card_id,
                }
