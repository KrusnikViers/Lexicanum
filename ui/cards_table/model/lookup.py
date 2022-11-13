from typing import List

from PySide6.QtCore import QModelIndex
from PySide6.QtGui import QColor

from app.data import Card
from ui.cards_table.model.abstract import AbstractCardsModel
from ui.cards_table.model.summary import SummaryCardsModel
from ui.shared.shortcuts import ShortcutCommand


class LookupCardsModel(AbstractCardsModel):
    def __init__(self, suggestions: List[Card], summary_model: SummaryCardsModel):
        super(LookupCardsModel, self).__init__()
        self.suggestions: List[Card] = suggestions
        self.summary_model:SummaryCardsModel = summary_model


    def card_by_row(self, row: int) -> Card:
        return self.suggestions[row]

    def highlight_color(self, index: QModelIndex) -> QColor | None:
        return None

    def row_count(self) -> int:
        return len(self.suggestions)

    def supports_invalid_card_type(self) -> bool:
        return False

    def execute_shortcut_action(self, row: int, command: ShortcutCommand):
        pass
