from typing import List

from PySide6.QtCore import QModelIndex

from core.types import Card, CardType
from ui.main_window.card_tables.base.model import CardsTableModel


class InputCardsTableModel(CardsTableModel):
    def __init__(self):
        super().__init__()
        self.input_cards: List[Card] = self._get_default_input()

    # Virtual methods
    def get_card(self, row: int) -> Card:
        return self.input_cards[row]

    def insert_card(self, card: Card):
        assert card.validity_status()
        self.beginInsertRows(QModelIndex(), 0, 0)
        self.input_cards.insert(0, card)
        self.endInsertRows()

    def remove_card(self, index: QModelIndex):
        row = index.row()
        self.beginRemoveRows(QModelIndex(), row, row)
        assert 0 <= row <= len(self.input_cards)
        del self.input_cards[row]
        self.endRemoveRows()

    def cards_count(self) -> int:
        return len(self.input_cards)

    def supports_invalid_card_type(self) -> bool:
        return True

    # Own methods
    @staticmethod
    def _get_default_input() -> List[Card]:
        return [Card(CardType.Invalid, question='', question_grammar_forms='', answer='', note='')]

    def reset_content(self, cards: List[Card] | None = None):
        self.beginResetModel()
        self.input_cards = cards if cards else self._get_default_input()
        self.endResetModel()
