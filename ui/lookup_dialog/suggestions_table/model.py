from typing import List

from PySide6.QtCore import QModelIndex
from PySide6.QtGui import QColor

from core.helpers import Status
from core.types import Card
from ui.common.cards_table.model import CardsTableModel


class SuggestionCardsTableModel(CardsTableModel):
    def __init__(self, suggestion_cards: List[Card]):
        super(SuggestionCardsTableModel, self).__init__()
        self.cards: List[Card] = suggestion_cards

    def highlight_color(self, index: QModelIndex) -> QColor | None:
        return None

    def supports_invalid_card_type(self) -> bool:
        return False

    # All contents should be filled during the construction.
    def add_card(self, card: Card) -> Status:
        raise NotImplementedError

    def get_card(self, row: int) -> Card:
        return self.cards[row]

    def remove_card(self, row: int):
        self.beginRemoveRows(QModelIndex(), row, row)
        del self.cards[row]
        self.endRemoveRows()

    def cards_count(self) -> int:
        return len(self.cards)
