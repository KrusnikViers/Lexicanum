from typing import List

from PySide6.QtCore import QModelIndex

from app.data.card import Card
from ui.cards_model.generic import GenericCardsModel
from ui.cards_model.summary import SummaryCardsModel
from ui.shortcuts import ShortcutCommand


class LookupCardsModel(GenericCardsModel):
    def __init__(self, suggestions: List[Card], summary_model: SummaryCardsModel):
        super(LookupCardsModel, self).__init__()
        self.suggestions = suggestions
        self.summary_model = summary_model

    def card_by_row(self, row: int) -> Card:
        return self.suggestions[row]

    def shortcut_action(self, row: int, command: ShortcutCommand):
        if command in (ShortcutCommand.ENTER, ShortcutCommand.ENTER_AND_CONTINUE):
            self.summary_model.new_row(self.suggestions[row])
        if command == ShortcutCommand.CLEAR:
            self.beginRemoveRows(QModelIndex(), row, row)
            del self.suggestions[row]
            self.endInsertRows()
            self.update_view(row)

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self.suggestions)
