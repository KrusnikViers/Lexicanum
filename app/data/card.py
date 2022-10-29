from enum import Enum
from typing import Optional

from PySide6.QtCore import QDateTime


class CardType(Enum):
    # Internal value
    Invalid = 0

    # Parts of speech
    Noun = 1
    Adjective = 2
    Verb = 3
    Adverb = 10
    Particle = 11

    # Complex concepts
    Phrase = 100
    Ordering = 101


class Card:
    def __init__(self, card_type: CardType,
                 question: str, answer: str,
                 note: Optional[str] = None, card_id: Optional[int] = None, created_at_sec: Optional[int] = None):
        assert card_type is not CardType.Invalid
        self.card_type = card_type
        self.question = question
        self.answer = answer
        self.note = note
        self.card_id = card_id
        self.created_at_sec = created_at_sec if created_at_sec is not None else QDateTime.currentSecsSinceEpoch()

    @classmethod
    def from_dict(cls, card_dict: dict):
        return cls(CardType(card_dict['card_type']),
                   card_dict['question'],
                   card_dict['answer'],
                   card_dict['note'],
                   card_dict['card_id'],
                   card_dict['created_at_sec'])

    def to_dict(self) -> dict:
        return {'card_type': self.card_type.value,
                'question': self.question,
                'answer': self.answer,
                'note': self.note,
                'card_id': self.card_id,
                'created_at_sec': self.created_at_sec,
                }
