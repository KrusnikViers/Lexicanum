from PySide6.QtCore import QModelIndex
from PySide6.QtGui import QColor

from core.types import Card, CardType
from core.util import Status
from ui.common.cards_table import CardsTableModel


class InputCardsTableModel(CardsTableModel):
    def __init__(self):
        super(InputCardsTableModel, self).__init__()
        self.input_card: Card = Card(CardType.Invalid, '', '', '')

    def highlight_color(self, index: QModelIndex) -> QColor | None:
        return None

    # This model should always have exactly one card.
    def add_card(self, card: Card) -> Status:
        raise NotImplementedError

    def remove_card(self, row: int):
        raise NotImplementedError

    def get_card(self, row: int) -> Card:
        assert row == 0
        return self.input_card

    def get_input_card(self) -> Card:
        return self.input_card

    def cards_count(self) -> int:
        return 1

    def supports_invalid_card_type(self) -> bool:
        return True

    def reset_data(self):
        self.input_card.card_type = CardType.Invalid
        self.input_card.question = ''
        self.input_card.answer = ''
        self.input_card.note = ''
        self.refresh_visible_contents(0)
