from enum import Enum

from typing import Optional


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
                 note: Optional[str] = None, card_id: Optional[int] = None):
        assert card_type is not CardType.Invalid
        self.card_type = card_type
        self.question = question
        self.answer = answer
        self.note = note
        self.card_id = card_id

    @classmethod
    def from_dict(cls, card_dict: dict):
        return cls(CardType(card_dict['card_type']),
                   card_dict['question'],
                   card_dict['answer'],
                   card_dict['note'],
                   card_dict['card_id'])

    def to_dict(self) -> dict:
        return {'card_type': self.card_type.value,
                'question': self.question,
                'answer': self.answer,
                'note': self.note,
                'card_id': self.card_id}
