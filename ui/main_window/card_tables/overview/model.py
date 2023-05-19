from copy import deepcopy
from typing import Any

from PySide6.QtCore import QModelIndex, Signal

from core.types import Deck, Card
from ui.main_window.card_tables.base.model import CardsTableModel


class OverviewCardsTableModel(CardsTableModel):
    deck_updated = Signal()

    def __init__(self, displayed_deck: Deck):
        super().__init__()
        self.deck: Deck = displayed_deck
        self.reset_deck(displayed_deck)

    # Virtual methods
    def supports_invalid_card_type(self) -> bool:
        return False

    def get_card(self, row: int) -> Card:
        return self.deck.cards[row]

    def cards_count(self) -> int:
        return len(self.deck.cards)

    # Own methods
    def setData(self, index: QModelIndex, value: Any, role: int = None) -> bool:
        result = super().setData(index, value, role)
        return result

    def add_card(self, card: Card):
        assert card.is_valid()
        self.beginInsertRows(QModelIndex(), 0, 0)
        self.deck.cards.insert(0, deepcopy(card))
        self.endInsertRows()

    def remove_card(self, index: QModelIndex):
        row = index.row()
        self.beginRemoveRows(QModelIndex(), row, row)
        assert 0 <= row <= len(self.deck.cards)
        del self.deck.cards[row]
        self.endRemoveRows()

    def reset_deck(self, new_deck: Deck):
        self.beginResetModel()
        self.deck = new_deck
        self.endResetModel()
