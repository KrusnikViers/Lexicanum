from enum import Enum
from typing import Optional


class CardType(Enum):
    Invalid = 0
    Noun = 1
    Ordering = 10
    Phrase = 11


class Language(Enum):
    EN = 1
    DE = 2


class Card:
    def __init__(self, card_type: CardType, question: str, answer: str, note: Optional[str] = None):
        self.card_type = card_type
        self.question = question
        self.answer = answer
        self.note = note
