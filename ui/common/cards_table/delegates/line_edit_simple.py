from PySide6.QtCore import QModelIndex, QAbstractItemModel, Qt
from PySide6.QtWidgets import QStyledItemDelegate, QWidget, QStyleOptionViewItem, QLineEdit


class LineEditSimpleDelegate(QStyledItemDelegate):
    instance = None

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> QWidget:
        return QLineEdit(parent)

    def setEditorData(self, editor: QLineEdit, index: QModelIndex) -> None:
        editor.setText(index.data(Qt.DisplayRole))

    def setModelData(self, editor: QLineEdit, model: QAbstractItemModel, index: QModelIndex) -> None:
        model.setData(index, editor.text(), Qt.DisplayRole)


LineEditSimpleDelegate.instance = \
    LineEditSimpleDelegate() if LineEditSimpleDelegate.instance is None else LineEditSimpleDelegate.instance
