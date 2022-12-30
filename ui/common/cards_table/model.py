from typing import Optional, Any

from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, QObject
from PySide6.QtGui import QColor

from core.types import Card, CardType
from core.util import Status, if_none
from ui.common.cards_table.header import CardsTableHeader


class CardsTableModel(QAbstractTableModel):
    def __init__(self, parent: QObject | None = None):
        super(CardsTableModel, self).__init__(parent)

    # Virtual methods
    def get_card(self, row: int) -> Card:
        raise NotImplementedError

    def add_card(self, card: Card) -> Status:
        raise NotImplementedError

    def remove_card(self, row: int):
        raise NotImplementedError

    def cards_count(self) -> int:
        raise NotImplementedError

    def highlight_color(self, index: QModelIndex) -> QColor | None:
        raise NotImplementedError

    def supports_invalid_card_type(self) -> bool:
        raise NotImplementedError

    # Common methods
    def refresh_visible_contents(self, row_from: int, row_to: int | None = None):
        row_to = if_none(row_to, row_from)
        self.dataChanged.emit(
            self.index(row_from, CardsTableHeader.Type.value, QModelIndex()),
            self.index(row_to, CardsTableHeader.Note.value, QModelIndex()),
            Qt.DisplayRole
        )

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        return Qt.ItemIsEnabled | Qt.ItemIsEditable

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(CardsTableHeader)

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return self.cards_count()

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = None) -> Optional[str]:
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return CardsTableHeader.of(section).name

    def setData(self, index: QModelIndex, value: Any, role: int = None) -> bool:
        if role != Qt.DisplayRole:
            return False
        card = self.get_card(index.row())
        match CardsTableHeader.of(index.column()):
            case CardsTableHeader.Type:
                assert isinstance(value, CardType)
                card.card_type = value
            case CardsTableHeader.Question:
                assert isinstance(value, str)
                card.question = value
            case CardsTableHeader.Answer:
                assert isinstance(value, str)
                card.answer = value
            case CardsTableHeader.Note:
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
        match CardsTableHeader.of(index.column()):
            case CardsTableHeader.Type:
                return card.card_type.display_name()
            case CardsTableHeader.Question:
                return card.question
            case CardsTableHeader.Answer:
                return card.answer
            case CardsTableHeader.Note:
                return card.note
        assert False
