from typing import List
from typing import Optional

from PySide6.QtCore import QDateTime

from app.data.base.card import Card
from app.data.stored.path import Path


class Deck:
    def __init__(self, deck_name: str, cards: List[Card],
                 next_card_id: Optional[int] = None, deck_id: Optional[int] = None, file_path: Optional[Path] = None):
        self.deck_id: int | None = deck_id
        self.deck_name: str = deck_name
        self.cards: List[Card] = cards
        # Next card id is strictly incremental, because this is the only way Anki tells cards apart. If id will
        # be reassigned after card was deleted from the project, Anki will attach previous history for this id to
        # the new card.
        self.next_card_id: int = next_card_id if next_card_id is not None else 0
        self.file_path: Path | None = file_path

    def to_dict(self) -> dict:
        assert self.deck_id is not None  # Call |normalize_for_output| beforehand.
        return {
            'deck_id': self.deck_id,
            'deck_name': self.deck_name,
            'next_card_id': self.next_card_id,
            'cards': [card.to_dict() for card in self.cards]
        }

    @classmethod
    def from_dict(cls, input_dict: dict, file_path: Path | None) -> 'Deck':
        return cls(deck_id=input_dict['deck_id'],
                   deck_name=input_dict['deck_name'],
                   next_card_id=input_dict['next_card_id'],
                   cards=[Card.from_dict(card_input) for card_input in input_dict['cards']],
                   file_path=file_path)

    def normalize_for_output(self):
        if self.deck_id is None:
            self.deck_id = hash(QDateTime.currentMSecsSinceEpoch()) % 10000000000
        for card in self.cards:
            if card.card_id is None:
                card.card_id = self.next_card_id
                self.next_card_id += 1
            card.answer = card.answer.strip()
            card.question = card.question.strip()
            card.note = card.note.strip()
