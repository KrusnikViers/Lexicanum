from enum import Enum
from typing import Optional, Any

from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, QObject
from PySide6.QtGui import QColor

from app.data import Card, CardType, Status


class CardsModelHeader(Enum):
    Type = 0
    Question = 1
    Answer = 2
    Note = 3

    @classmethod
    def of(cls, index: int) -> 'CardsModelHeader':
        match index:
            case 0:
                return cls.Type
            case 1:
                return cls.Question
            case 2:
                return cls.Answer
            case 3:
                return cls.Note
        assert False


class BaseCardsModel(QAbstractTableModel):
    def __init__(self, parent: QObject | None = None):
        super(BaseCardsModel, self).__init__(parent)

    # These methods are to be reimplemented in the child classes.
    #############################################################
    def get_card(self, row: int) -> Card:
        raise NotImplementedError

    def add_card(self, card: Card) -> Status:
        raise NotImplementedError

    def remove_card(self, row: int):
        raise NotImplementedError

    def cards_count(self) -> int:
        raise NotImplementedError

    def highlight_color(self, index: QModelIndex) -> QColor | None:
        return None

    def supports_invalid_card_type(self) -> bool:
        return False

    # Common logic for all models.
    ##############################
    def refresh_visible_contents(self, row_from: int, row_to: int | None = None):
        if row_to is None:
            row_to = row_from
        self.dataChanged.emit(
            self.index(row_from, CardsModelHeader.Type.value, QModelIndex()),
            self.index(row_to, CardsModelHeader.Note.value, QModelIndex()),
            Qt.DisplayRole
        )

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        return Qt.ItemIsEnabled | Qt.ItemIsEditable

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(CardsModelHeader)

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return self.cards_count()

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = None) -> Optional[str]:
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return CardsModelHeader.of(section).name

    def setData(self, index: QModelIndex, value: Any, role: int = None) -> bool:
        if role != Qt.DisplayRole:
            return False
        card = self.get_card(index.row())
        match CardsModelHeader.of(index.column()):
            case CardsModelHeader.Type:
                assert isinstance(value, CardType)
                card.card_type = value
            case CardsModelHeader.Question:
                assert isinstance(value, str)
                card.question = value
            case CardsModelHeader.Answer:
                assert isinstance(value, str)
                card.answer = value
            case CardsModelHeader.Note:
                assert isinstance(value, str)
                card.note = value
        self.refresh_visible_contents(index.row())
        return True

    def data(self, index: QModelIndex, role: int = None) -> str | None:
        if role == Qt.BackgroundRole:
            return self.highlight_color(index)
        if role != Qt.DisplayRole:
            return None

        card = self.get_card(index.row())
        match CardsModelHeader.of(index.column()):
            case CardsModelHeader.Type:
                return card.card_type.name if card.card_type is not CardType.Invalid else ''
            case CardsModelHeader.Question:
                return card.question
            case CardsModelHeader.Answer:
                return card.answer
            case CardsModelHeader.Note:
                return card.note
        assert False
