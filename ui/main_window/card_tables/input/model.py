from typing import List

from PySide6.QtCore import QModelIndex

from core.types import Card, CardType
from ui.main_window.card_tables.base.model import CardsTableModel


class InputCardsTableModel(CardsTableModel):
    def __init__(self):
        super().__init__()
        self.input_cards: List[Card] = self.get_default_input()

    # Virtual methods
    def get_card(self, row: int) -> Card:
        return self.input_cards[row]

    def cards_count(self) -> int:
        return len(self.input_cards)

    def supports_invalid_card_type(self) -> bool:
        return True

    # Own methods
    @staticmethod
    def get_default_input() -> List[Card]:
        return [Card(CardType.Invalid, question='', question_grammar_forms='', answer='', note='')]

    def reset_data(self):
        is_extra_rows_removed = (len(self.input_cards) > 1)
        if is_extra_rows_removed:
            self.beginRemoveRows(QModelIndex(), 1, len(self.input_cards) - 1)
        self.input_cards = self.get_default_input()
        if is_extra_rows_removed:
            self.endRemoveRows()
        self.refresh_visible_contents(0)
