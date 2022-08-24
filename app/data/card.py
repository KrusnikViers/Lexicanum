from enum import Enum
from typing import Optional


class CardIdGenerator:
    _last_id = 0

    @classmethod
    def get(cls):
        id_to_return = cls._last_id
        cls._last_id += 1
        return id_to_return

    @classmethod
    def get_last_id(cls):
        return cls._last_id

    @classmethod
    def set_last_id(cls, last_id: int):
        cls._last_id = last_id


class CardType(Enum):
    # Internal value
    Invalid = 0

    # Parts of speech
    Noun = 1

    # Complex concepts
    Phrase = 100
    Ordering = 101


class Card:
    def __init__(self, card_type: CardType,
                 question: str, answer: str,
                 note: Optional[str] = '', card_id: Optional[int] = None):
        assert card_type is not CardType.Invalid
        self.card_type = card_type
        self.question = question
        self.answer = answer
        self.note = note
        self.card_id = CardIdGenerator.get() if card_id is None else card_id

    @classmethod
    def from_dict(cls, card_dict: dict):
        return cls(CardType(card_dict['card_type']),
                   card_dict['question'], card_dict['answer'],
                   card_dict['note'], card_dict['card_id'])

    def to_dict(self) -> dict:
        return {
            'card_type': self.card_type.value,
            'question': self.question,
            'answer': self.answer,
            'note': self.note,
            'card_id': self.card_id
        }
