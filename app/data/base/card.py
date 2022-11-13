from enum import Enum
from typing import Optional


class CardType(Enum):
    # Internal value
    Invalid = 0

    # Major parts of speech
    Noun = 1
    Adjective = 2
    Verb = 3
    Adverb = 4

    # Minor parts of speech
    Particle = 11
    Conjunction = 12
    Pronoun = 13
    Interjection = 14

    # Complex concepts
    Phrase = 100
    Ordering = 101
    Form = 102


class Card:
    def __init__(self, card_type: CardType,
                 question: str, answer: str, note: str,
                 card_id: Optional[int] = None):
        self.card_type: CardType = card_type
        self.question: str = question
        self.answer: str = answer
        self.note: str = note
        self.card_id: int | None = card_id

    @classmethod
    def from_dict(cls, card_dict: dict) -> 'Card':
        return cls(CardType(card_dict['card_type']),
                   card_dict['question'],
                   card_dict['answer'],
                   card_dict['note'],
                   card_dict['card_id'])

    def to_dict(self) -> dict:
        # Should be assigned by deck beforehand.
        assert self.card_id is not None
        assert self.card_type is not CardType.Invalid
        return {'card_type': self.card_type.value,
                'question': self.question,
                'answer': self.answer,
                'note': self.note,
                'card_id': self.card_id,
                }
