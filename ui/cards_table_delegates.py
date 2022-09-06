from PySide2.QtCore import QModelIndex, QAbstractItemModel, Qt
from PySide2.QtWidgets import QStyledItemDelegate, QWidget, QStyleOptionViewItem, QComboBox, QLineEdit

from app.data.card import CardType
from ui.cards_table_model import CardsTableModel
from ui.gen.line_edit_with_lookup_uic import Ui_LineEditWithLookup


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


class CardStringLookupDelegate(QStyledItemDelegate):
    class Widget(QWidget):
        def __init__(self, parent: QWidget):
            super(CardStringLookupDelegate.Widget, self).__init__(parent)
            self.ui = Ui_LineEditWithLookup()
            self.ui.setupUi(self)

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> QWidget:
        return self.Widget(parent)

    def setEditorData(self, editor: QWidget, index: QModelIndex) -> None:
        assert isinstance(editor, self.Widget)
        editor.ui.line_edit.setText(index.data(Qt.DisplayRole))

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex) -> None:
        assert isinstance(editor, self.Widget)
        model.setData(index, editor.ui.line_edit.text(), Qt.DisplayRole)
