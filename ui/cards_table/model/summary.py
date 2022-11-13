from copy import deepcopy

from PySide6.QtCore import QModelIndex
from PySide6.QtGui import QColor

from app.data import Card, Deck
from ui.cards_table.model.abstract import AbstractCardsModel
from ui.shared.shortcuts import ShortcutCommand


class SummaryCardsModel(AbstractCardsModel):
    def __init__(self, displayed_deck: Deck):
        super(SummaryCardsModel, self).__init__()
        self.deck = displayed_deck

    def highlight_color(self, index: QModelIndex) -> QColor | None:
        return None

    def supports_invalid_card_type(self) -> bool:
        return False

    def row_count(self) -> int:
        return len(self.deck.cards)

    def card_by_row(self, row: int) -> Card:
        return self.deck.cards[row]

    def execute_shortcut_action(self, row: int, command: ShortcutCommand):
        pass

    def remove_row(self, row: int) -> None:
        assert 0 < row <= len(self.deck.cards)
        self.beginRemoveRows(QModelIndex(), row, row)
        del self.deck.cards[row - 1]
        self.endRemoveRows()

    def new_row(self, card: Card):
        _ROW_INDEX = 1
        self.beginInsertRows(QModelIndex(), _ROW_INDEX, _ROW_INDEX)
        self.deck.cards.insert(0, deepcopy(card))
        self.endInsertRows()
        self.refresh_visible_contents(_ROW_INDEX)
