from PySide6.QtCore import QModelIndex, QAbstractItemModel, Qt
from PySide6.QtWidgets import QStyledItemDelegate, QWidget, QStyleOptionViewItem, QComboBox

from app.data.card import CardType
from ui.cards_table.model.abstract import AbstractCardsModel


class CardTypeDelegate(QStyledItemDelegate):
    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> QWidget:
        editor = QComboBox(parent)
        for card_type in CardType:
            if card_type != CardType.Invalid:
                editor.addItem(card_type.name, userData=card_type)
        return editor

    def setEditorData(self, editor: QWidget, index: QModelIndex) -> None:
        assert isinstance(editor, QComboBox)
        assert isinstance(index.model(), AbstractCardsModel)
        type_to_choose = index.model().card_by_row(index.row()).card_type
        for selection_index in range(0, editor.count()):
            if editor.itemData(selection_index, role=Qt.UserRole) == type_to_choose:
                editor.setCurrentIndex(selection_index)
                break

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex) -> None:
        assert isinstance(editor, QComboBox)
        model.setData(index, editor.currentData(Qt.UserRole), Qt.DisplayRole)