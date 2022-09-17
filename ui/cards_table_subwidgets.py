from PySide2.QtCore import QModelIndex, QAbstractItemModel, Qt
from PySide2.QtWidgets import QStyledItemDelegate, QWidget, QStyleOptionViewItem, QComboBox, QLineEdit, QPushButton

from app.data.card import CardType
from ui.cards_table_model import CardsTableModel
from ui.icons.icons import SharedIcons


class CardTypeDelegate(QStyledItemDelegate):
    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> QWidget:
        editor = QComboBox(parent)
        for card_type in CardType:
            if card_type != CardType.Invalid:
                editor.addItem(card_type.name, userData=card_type)
        return editor

    def setEditorData(self, editor: QWidget, index: QModelIndex) -> None:
        assert isinstance(editor, QComboBox)
        assert isinstance(index.model(), CardsTableModel)
        type_to_choose = index.model().card_by_row(index.row()).card_type
        for selection_index in range(0, editor.count()):
            if editor.itemData(selection_index, role=Qt.UserRole) == type_to_choose:
                editor.setCurrentIndex(selection_index)
                break

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex) -> None:
        assert isinstance(editor, QComboBox)
        model.setData(index, editor.currentData(Qt.UserRole), Qt.DisplayRole)


class CardPlainStringDelegate(QStyledItemDelegate):
    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> QWidget:
        return QLineEdit(parent)

    def setEditorData(self, editor: QWidget, index: QModelIndex) -> None:
        assert isinstance(editor, QLineEdit)
        editor.setText(index.data(Qt.DisplayRole))

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex) -> None:
        assert isinstance(editor, QLineEdit)
        model.setData(index, editor.text(), Qt.DisplayRole)


class CardActButton(QPushButton):
    def __init__(self, parent: QWidget, row_number: int):
        super(CardActButton, self).__init__(parent)
        self.setStyleSheet('border: 0px;')
        self.setIcon(SharedIcons.Plus if row_number == 0 else SharedIcons.Trash)
        self.row_number = row_number
