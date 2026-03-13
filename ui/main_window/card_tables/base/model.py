from typing import Optional, Any

from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, QObject

from core.types import Card, CardType
from core.util import if_none
from ui.main_window.card_tables.base.header import CardsTableHeader


class CardsTableModel(QAbstractTableModel):
    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)

    # Virtual methods
    def get_card(self, row: int) -> Card:
        raise NotImplementedError

    def insert_card(self, card: Card):
        raise NotImplementedError

    def remove_card(self, index: QModelIndex):
        raise NotImplementedError

    def cards_count(self) -> int:
        raise NotImplementedError

    def supports_invalid_card_type(self) -> bool:
        raise NotImplementedError

    # Common methods, shared by all derived classes
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
            return CardsTableHeader.of(section).display_name()

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
                card.question_main = value
            case CardsTableHeader.Grammar:
                assert isinstance(value, str)
                card.question_grammar = value
            case CardsTableHeader.IPA:
                assert isinstance(value, str)
                card.question_ipa = value
            case CardsTableHeader.QExample:
                assert isinstance(value, str)
                card.question_example = value
            case CardsTableHeader.Answer:
                assert isinstance(value, str)
                card.answer_main = value
            case CardsTableHeader.AExample:
                assert isinstance(value, str)
                card.answer_example = value
            case CardsTableHeader.Note:
                assert isinstance(value, str)
                card.card_note = value
        self.refresh_visible_contents(index.row())
        return True

    def data(self, index: QModelIndex, role: int = None) -> str | None:
        if role != Qt.DisplayRole:
            return None

        card = self.get_card(index.row())
        match CardsTableHeader.of(index.column()):
            case CardsTableHeader.Type:
                return card.card_type.display_name()
            case CardsTableHeader.Question:
                return card.question_main
            case CardsTableHeader.Grammar:
                return card.question_grammar
            case CardsTableHeader.IPA:
                return card.question_ipa
            case CardsTableHeader.QExample:
                return card.question_example
            case CardsTableHeader.Answer:
                return card.answer_main
            case CardsTableHeader.AExample:
                return card.answer_example
            case CardsTableHeader.Note:
                return card.card_note
        assert False
