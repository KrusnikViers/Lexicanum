from enum import Enum
from typing import Optional, List

from PySide2.QtCore import QDateTime


class CardType(Enum):
    # Internal value
    Invalid = 0

    # Parts of speech
    Noun = 1

    # Complex concepts
    Phrase = 10
    Ordering = 11


class Card:
    def __init__(self, card_type: CardType, question: str, answer: str,
                 note: Optional[str] = '', time_id: Optional[int] = None):
        assert card_type is not CardType.Invalid
        self.time_id = time_id if time_id is not None else QDateTime.currentMSecsSinceEpoch()
        self.card_type = card_type
        self.question = question
        self.answer = answer
        self.note = note

    def to_str_list(self) -> List[str]:
        return [str(self.time_id), self.question, self.answer, self.note, str(self.card_type.value)]

    @classmethod
    def from_str_list(cls, input_list: List[str]):
        return cls(CardType(int(input_list[4])), input_list[1], input_list[2], input_list[3], int(input_list[0]))
