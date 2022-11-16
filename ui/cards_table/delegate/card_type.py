from PySide6.QtCore import QModelIndex, QAbstractItemModel, Qt, Slot
from PySide6.QtWidgets import QStyledItemDelegate, QWidget, QStyleOptionViewItem, QComboBox

from app.data import CardType
from ui.cards_table.model.base import BaseCardsModel


class CardTypeDelegate(QStyledItemDelegate):
    instance = None

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> QWidget:
        editor = QComboBox(parent)
        assert isinstance(index.model(), BaseCardsModel)

        for card_type in CardType:
            if card_type == CardType.Invalid:
                if index.model().supports_invalid_card_type():
                    editor.addItem('', userData=CardType.Invalid)
                    editor.insertSeparator(len(CardType))
                continue

            if card_type in (CardType.Particle, CardType.Phrase):
                editor.insertSeparator(len(CardType))
            editor.addItem(card_type.name, userData=card_type)
        editor.currentIndexChanged.connect(self.on_selection_changed)
        return editor

    def setEditorData(self, editor: QWidget, index: QModelIndex) -> None:
        assert isinstance(editor, QComboBox)
        assert isinstance(index.model(), BaseCardsModel)
        type_to_choose = index.model().get_card(index.row()).card_type
        for selection_index in range(0, editor.count()):
            if editor.itemData(selection_index, role=Qt.UserRole) == type_to_choose:
                editor.setCurrentIndex(selection_index)
                break

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex) -> None:
        assert isinstance(editor, QComboBox)
        model.setData(index, editor.currentData(Qt.UserRole), Qt.DisplayRole)

    @Slot()
    def on_selection_changed(self):
        self.commitData.emit(self.sender())


CardTypeDelegate.instance = \
    CardTypeDelegate() if CardTypeDelegate.instance is None else CardTypeDelegate.instance
