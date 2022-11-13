from PySide6.QtCore import QModelIndex
from PySide6.QtGui import QColor

from app.data import Card, CardType
from ui.cards_table.model.abstract import AbstractCardsModel
from ui.cards_table.model.summary import SummaryCardsModel
from ui.shared.shortcuts import ShortcutCommand


class InputCardsModel(AbstractCardsModel):
    def __init__(self, summary_model: SummaryCardsModel):
        super(InputCardsModel, self).__init__()
        self.summary_model = summary_model
        self.input_card: Card = Card(CardType.Invalid, '', '', '')

    def card_by_row(self, row: int) -> Card:
        assert row == 0
        return self.input_card

    def execute_shortcut_action(self, row: int, command: ShortcutCommand):
        pass

    def highlight_color(self, index: QModelIndex) -> QColor | None:
        return None

    def supports_invalid_card_type(self) -> bool:
        return True

    def row_count(self) -> int:
        return 1
