from typing import List

from PySide6.QtCore import QModelIndex

from app.data import Card
from ui.cards_table.model.abstract import AbstractCardsModel
from ui.cards_table.model.summary import SummaryCardsModel
from ui.shared.shortcuts import ShortcutCommand


class LookupCardsModel(AbstractCardsModel):
    def __init__(self, suggestions: List[Card], summary_model: SummaryCardsModel):
        super(LookupCardsModel, self).__init__()
        self.suggestions: List[Card] = suggestions
        self.summary_model:SummaryCardsModel = summary_model

    def supports_invalid_card_type(self) -> bool:
        return False

    def card_by_row(self, row: int) -> Card:
        return self.suggestions[row]

    def execute_shortcut_action(self, row: int, command: ShortcutCommand):
        if command in (ShortcutCommand.ENTER, ShortcutCommand.ENTER_AND_CONTINUE):
            self.summary_model.new_row(self.suggestions[row])
        if command == ShortcutCommand.CLEAR:
            self.beginRemoveRows(QModelIndex(), row, row)
            del self.suggestions[row]
            self.endInsertRows()
            self.refresh_visible_contents(row)

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self.suggestions)
