from typing import List
from typing import Optional

from PySide6.QtCore import QDateTime

from app.data.card import Card
from app.data.storage.path import Path


class Deck:
    def __init__(self, deck_name: str, cards: List[Card],
                 next_card_id: Optional[int] = None, deck_id: Optional[int] = None, file_path: Optional[Path] = None):
        self.deck_id = deck_id
        self.deck_name = deck_name
        self.next_card_id = next_card_id
        self.cards = cards
        self.file_path = file_path

    def normalize_for_output(self):
        if self.next_card_id is None:
            self.next_card_id = 0
        if self.deck_id is None:
            self.deck_id = hash(QDateTime.currentMSecsSinceEpoch()) % 10000000000
        for card in self.cards:
            if card.card_id is None:
                card.card_id = self.next_card_id
                self.next_card_id += 1
            if card.note is None:
                card.note = ''
