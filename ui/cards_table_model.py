from typing import Optional

from PySide2.QtCore import Qt, QAbstractTableModel, QModelIndex

from app.data.deck import Deck

_HEADERS = ['Type', 'Question', 'Answer', 'Note']


class CardsTableModel(QAbstractTableModel):
    def __init__(self, displayed_deck: Deck):
        super(CardsTableModel, self).__init__()
        self.deck = displayed_deck

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        # First row is a "fake one", to add new records.
        return len(self.deck.cards) + 1

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(_HEADERS)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = None) -> Optional[str]:
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return _HEADERS[section]
        if orientation == Qt.Vertical:
            return '+' if section == 0 else str(section)

    def data(self, index: QModelIndex, role: int = None) -> Optional[str]:
        if index.row() == 0:
            return 'TEMP'
        card = self.deck.cards[index.row() - 1]
        if index.column() == 0:
            return card.card_type.name
        elif index.column() == 1:
            return card.question
        elif index.column() == 2:
            return card.answer
        elif index.column() == 3:
            return card.note
        assert False
