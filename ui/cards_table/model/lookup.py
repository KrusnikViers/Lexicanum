from typing import List

from PySide6.QtCore import QModelIndex

from app.data import Card, Status
from ui.cards_table.model.base import BaseCardsModel


class LookupCardsModel(BaseCardsModel):
    def __init__(self, suggestions: List[Card]):
        super(LookupCardsModel, self).__init__()
        self.suggestions: List[Card] = suggestions

    def add_card(self, card: Card) -> Status:
        raise NotImplementedError

    def get_card(self, row: int) -> Card:
        return self.suggestions[row]

    def remove_card(self, row: int):
        self.beginRemoveRows(QModelIndex(), row, row)
        del self.suggestions[row]
        self.endRemoveRows()

    def cards_count(self) -> int:
        return len(self.suggestions)
