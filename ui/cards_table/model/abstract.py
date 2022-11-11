from enum import Enum
from typing import Optional, Any

from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, QObject
from PySide6.QtGui import QColor

from app.data import Card, CardType
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
    def __init__(self, parent: QObject | None = None):
        super(AbstractCardsModel, self).__init__(parent)

    # These methods are to be reimplemented in the child classes.
    def card_by_row(self, row: int) -> Card:
        raise NotImplementedError

    def execute_shortcut_action(self, row: int, command: ShortcutCommand):
        raise NotImplementedError

    def highlight_color(self, index: QModelIndex) -> QColor | None:
        raise NotImplementedError

    def supports_invalid_card_type(self) -> bool:
        raise NotImplementedError

    # Common logic for all models.
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
        self.refresh_visible_contents(index.row())
        return True

    def data(self, index: QModelIndex, role: int = None) -> str | None:
        if role == Qt.BackgroundRole:
            return self.highlight_color(index)
        if role != Qt.DisplayRole:
            return None

        card = self.card_by_row(index.row())
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
