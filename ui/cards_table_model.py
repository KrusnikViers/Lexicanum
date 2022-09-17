from enum import Enum
from typing import Optional, Any

from PySide2.QtCore import Qt, QAbstractTableModel, QModelIndex

from app.data.card import Card, CardType
from app.data.deck import Deck


class CardsModelHeaders(Enum):
    Type = 0
    Question = 1
    Answer = 2
    Note = 3
    Act = 4


class CardsTableModel(QAbstractTableModel):
    HeadersByIndex = {header.value: header for header in CardsModelHeaders}

    def __init__(self, displayed_deck: Deck):
        super(CardsTableModel, self).__init__()
        self.deck = displayed_deck
        self.stub_card = Card(CardType.Phrase, '', '', '')

    def card_by_row(self, row: int) -> Card:
        return self.deck.cards[row - 1] if row > 0 else self.stub_card

    def act_on_row(self, row: int) -> None:
        QModelIndex()
        if row == 0:
            new_card = self.stub_card
            self.beginInsertRows(QModelIndex(), 1, 1)
            self.deck.cards.insert(0, new_card)
            self.endInsertRows()
        else:
            self.beginRemoveRows(QModelIndex(), row, row)
            del self.deck.cards[row - 1]
            self.endRemoveRows()

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        return Qt.ItemIsEnabled | Qt.ItemIsEditable

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        # First row is a stub, to add new records.
        return len(self.deck.cards) + 1

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(CardsModelHeaders)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = None) -> Optional[str]:
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return self.HeadersByIndex[section].name
        if orientation == Qt.Vertical:
            return 'New' if section == 0 else str(section)

    def setData(self, index: QModelIndex, value: Any, role: int = None) -> bool:
        if role != Qt.DisplayRole:
            return False
        card = self.card_by_row(index.row())
        match self.HeadersByIndex[index.column()]:
            case CardsModelHeaders.Type:
                assert isinstance(value, CardType)
                card.card_type = value
            case CardsModelHeaders.Question:
                assert isinstance(value, str)
                card.question = value.strip()
            case CardsModelHeaders.Answer:
                assert isinstance(value, str)
                card.answer = value.strip()
            case CardsModelHeaders.Note:
                assert isinstance(value, str)
                card.note = value.strip()
            case CardsModelHeaders.Act:
                pass
        return True

    def data(self, index: QModelIndex, role: int = None) -> str | None:
        if role != Qt.DisplayRole:
            return None

        card = self.card_by_row(index.row())
        match self.HeadersByIndex[index.column()]:
            case CardsModelHeaders.Type:
                return card.card_type.name
            case CardsModelHeaders.Question:
                return card.question
            case CardsModelHeaders.Answer:
                return card.answer
            case CardsModelHeaders.Note:
                return card.note
            case CardsModelHeaders.Act:
                return None
        assert False
