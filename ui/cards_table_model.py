from enum import Enum
from typing import Optional, Any

from PySide2.QtCore import Qt, QAbstractTableModel, QModelIndex

from app.data.card import Card, CardType
from app.data.deck import Deck


class CardAction(Enum):
    Delete = 1
    Add = 2


class CardsTableModel(QAbstractTableModel):
    class Headers(Enum):
        Type = 0
        Question = 1
        Answer = 2
        Note = 3
        Act = 4

    HeadersByIndex = {header.value: header for header in Headers}

    def __init__(self, displayed_deck: Deck):
        super(CardsTableModel, self).__init__()
        self.deck = displayed_deck
        self.stub_card = Card(CardType.Phrase, '', '', '')

    def card_by_row(self, row: int) -> Card:
        return self.deck.cards[row - 1] if row > 0 else self.stub_card

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        return Qt.ItemIsEnabled | Qt.ItemIsEditable

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        # First row is a stub, to add new records.
        return len(self.deck.cards) + 1

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self.Headers)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = None) -> Optional[str]:
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return self.HeadersByIndex[section].name
        if orientation == Qt.Vertical:
            return '+' if section == 0 else str(section)

    def setData(self, index: QModelIndex, value: Any, role: int = None) -> bool:
        if role != Qt.DisplayRole:
            return False
        card = self.card_by_row(index.row())
        if self.HeadersByIndex[index.column()] == self.Headers.Type:
            assert isinstance(value, CardType)
            card.card_type = value
            return True
        elif self.HeadersByIndex[index.column()] == self.Headers.Question:
            assert isinstance(value, str)
            card.question = value.strip()
            return True
        elif self.HeadersByIndex[index.column()] == self.Headers.Answer:
            assert isinstance(value, str)
            card.answer = value.strip()
            return True
        elif self.HeadersByIndex[index.column()] == self.Headers.Note:
            assert isinstance(value, str)
            card.note = value.strip()
            return True
        elif self.HeadersByIndex[index.column()] == self.Headers.Act:
            return True
        assert False

    def data(self, index: QModelIndex, role: int = None) -> str | CardAction | None:
        if role != Qt.DisplayRole:
            return None

        card = self.card_by_row(index.row())
        if self.HeadersByIndex[index.column()] == self.Headers.Type:
            return card.card_type.name
        elif self.HeadersByIndex[index.column()] == self.Headers.Question:
            return card.question
        elif self.HeadersByIndex[index.column()] == self.Headers.Answer:
            return card.answer
        elif self.HeadersByIndex[index.column()] == self.Headers.Note:
            return card.note
        elif self.HeadersByIndex[index.column()] == self.Headers.Act:
            return None
        assert False
