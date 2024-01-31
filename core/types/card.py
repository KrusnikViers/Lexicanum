from core.types.card_type import CardType

from core.util import Status


class Card:
    LINE_DELIMITER = ';'

    def __init__(self, card_type: CardType,
                 question_main: str, question_grammar: str, question_ipa: str, question_example: str,
                 answer_main: str, answer_example: str, card_note: str, card_id: int | None = None):
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
        self.card_note: str = card_note

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

    # Name of fields used for serialization/deserialization
    _FIELD_CARD_ID = 'card_id'
    _FIELD_CARD_TYPE = 'card_type'
    _FIELD_CARD_NOTE = 'card_note'
    _FIELD_Q_MAIN = 'question_main'
    _FIELD_Q_GRAMMAR = 'question_grammar'
    _FIELD_Q_IPA = 'question_ipa'
    _FIELD_Q_EXAMPLE = 'question_example'
    _FIELD_A_MAIN = 'answer_main'
    _FIELD_A_EXAMPLE = 'answer_example'

    @classmethod
    def _normalize_multiline(cls, original_line: str) -> str:
        normalized_delimiter = '{} '.format(cls.LINE_DELIMITER)
        return normalized_delimiter.join(line.strip() for line in original_line.split(cls.LINE_DELIMITER))

    def normalize_for_output(self):
        # Multiline strings
        self.question_main = self._normalize_multiline(self.question_main)
        self.question_grammar = self._normalize_multiline(self.question_grammar)
        self.question_example = self._normalize_multiline(self.question_example)
        self.answer_main = self._normalize_multiline(self.answer_main)
        self.answer_example = self._normalize_multiline(self.answer_example)
        self.card_note = self._normalize_multiline(self.card_note)

        # Rest of the fields
        self.question_ipa = self.question_ipa.strip()

    @classmethod
    def from_dict(cls, card_dict: dict) -> 'Card':
        return cls(
            # Required fields.
            card_type=CardType(card_dict[cls._FIELD_CARD_TYPE]),
            question_main=card_dict[cls._FIELD_Q_MAIN],
            answer_main=card_dict[cls._FIELD_A_MAIN],
            # Optional fields
            question_grammar=card_dict.get(cls._FIELD_Q_GRAMMAR, ''),
            question_ipa=card_dict.get(cls._FIELD_Q_IPA, ''),
            question_example=card_dict.get(cls._FIELD_Q_EXAMPLE, ''),
            answer_example=card_dict.get(cls._FIELD_A_EXAMPLE, ''),
            card_note=card_dict.get(cls._FIELD_CARD_NOTE, ''),
            card_id=card_dict.get(cls._FIELD_CARD_ID, None))

    def to_dict(self) -> dict:
        assert self.card_id is not None, "Missing deck normalization?"
        assert self.card_type is not CardType.Invalid, "Empty type should never be stored"
        return {
            self._FIELD_CARD_TYPE: self.card_type.value,
            self._FIELD_Q_MAIN: self.question_main,
            self._FIELD_Q_GRAMMAR: self.question_grammar,
            self._FIELD_Q_IPA: self.question_ipa,
            self._FIELD_Q_EXAMPLE: self.question_example,
            self._FIELD_A_MAIN: self.answer_main,
            self._FIELD_A_EXAMPLE: self.answer_example,
            self._FIELD_CARD_NOTE: self.card_note,
            self._FIELD_CARD_ID: self.card_id
        }
