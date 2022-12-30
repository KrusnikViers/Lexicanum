import time
from typing import List

from core.types.card import Card
from core.util import if_none, UniversalPath


class Deck:
    def __init__(self, deck_name: str, cards: List[Card],
                 next_card_id: int | None = None, deck_id: int | None = None, file_path: UniversalPath | None = None):
        self.deck_id: int | None = deck_id
        self.deck_name: str = deck_name
        self.cards: List[Card] = cards
        self.file_path: UniversalPath | None = file_path
        # Next card id is strictly incremental, because this is the only way Anki tells cards apart. If id will
        # be reassigned after card was deleted from the project, Anki will attach previous history for this id to
        # the new card.
        self.next_card_id: int = if_none(next_card_id, 0)

    def to_dict(self) -> dict:
        assert self.deck_id is not None, "Missing |normalize_for_output| call?"
        return {
            'deck_id': self.deck_id,
            'deck_name': self.deck_name,
            'next_card_id': self.next_card_id,
            'cards': [card.to_dict() for card in self.cards]
        }

    @classmethod
    def from_dict(cls, input_dict: dict, file_path: UniversalPath | None) -> 'Deck':
        return cls(deck_id=input_dict['deck_id'],
                   deck_name=input_dict['deck_name'],
                   next_card_id=input_dict['next_card_id'],
                   cards=[Card.from_dict(card_input) for card_input in input_dict['cards']],
                   file_path=file_path)

    def normalize_for_output(self):
        self.deck_id = if_none(self.deck_id, hash(time.time_ns()) % 10000000000)
        for card in self.cards:
            if card.card_id is None:
                card.card_id = self.next_card_id
                self.next_card_id += 1
            card.answer = card.answer.strip()
            card.question = card.question.strip()
            card.note = card.note.strip()
