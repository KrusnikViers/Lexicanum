from abc import abstractmethod, ABCMeta
from enum import Enum
from typing import Optional, Any

from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, QObject
from PySide6.QtGui import QColor

from app.data.card import Card, CardType
from ui.shared.shortcuts import ShortcutCommand


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


class AbstractCardsModel(QAbstractTableModel):
    __metaclass__ = ABCMeta

    def __init__(self, parent: QObject | None = None):
        super(AbstractCardsModel, self).__init__(parent)

    def update_view(self, row_from: int, row_to: int | None = None):
        if row_to is None:
            row_to = row_from
        self.dataChanged.emit(
            self.index(row_to, CardsModelHeader.Type.value, QModelIndex()),
            self.index(row_to, CardsModelHeader.Note.value, QModelIndex()),
            Qt.DisplayRole
        )

    @abstractmethod
    def card_by_row(self, row: int) -> Card:
        pass

    @abstractmethod
    def shortcut_action(self, row: int, command: ShortcutCommand):
        pass

    @abstractmethod
    def highlight_color(self, index: QModelIndex) -> QColor | None:
        return None

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        return Qt.ItemIsEnabled | Qt.ItemIsEditable

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(CardsModelHeader)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = None) -> Optional[str]:
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return CardsModelHeader.of(section).name

    def setData(self, index: QModelIndex, value: Any, role: int = None) -> bool:
        if role != Qt.DisplayRole:
            return False
        card = self.card_by_row(index.row())
        match CardsModelHeader.of(index.column()):
            case CardsModelHeader.Type:
                assert isinstance(value, CardType)
                card.card_type = value
            case CardsModelHeader.Question:
                assert isinstance(value, str)
                card.question = value.strip()
            case CardsModelHeader.Answer:
                assert isinstance(value, str)
                card.answer = value.strip()
            case CardsModelHeader.Note:
                assert isinstance(value, str)
                card.note = value.strip()
        self.update_view(index.row())
        return True

    def data(self, index: QModelIndex, role: int = None) -> str | None:
        if role == Qt.BackgroundRole:
            return self.highlight_color(index)
        if role != Qt.DisplayRole:
            return None

        card = self.card_by_row(index.row())
        match CardsModelHeader.of(index.column()):
            case CardsModelHeader.Type:
                return card.card_type.name
            case CardsModelHeader.Question:
                return card.question
            case CardsModelHeader.Answer:
                return card.answer
            case CardsModelHeader.Note:
                return card.note
        assert False
