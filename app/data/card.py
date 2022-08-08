from enum import Enum
from typing import Optional


class CardType(Enum):
    # Internal value
    Invalid = 0

    # Parts of speech
    Noun = 1

    # Complex concepts
    Phrase = 10
    Ordering = 11


class Card:
    def __init__(self, card_type: CardType, question: str, answer: str, note: Optional[str] = None):
        assert card_type is not CardType.Invalid
        self.card_type = card_type
        self.question = question
        self.answer = answer
        self.note = note
