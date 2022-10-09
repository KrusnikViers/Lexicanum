from PySide6.QtCore import QModelIndex, QAbstractItemModel, Qt
from PySide6.QtWidgets import QStyledItemDelegate, QWidget, QStyleOptionViewItem, QLineEdit


class LineEditSimpleDelegate(QStyledItemDelegate):
    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> QWidget:
        return QLineEdit(parent)

    def setEditorData(self, editor: QWidget, index: QModelIndex) -> None:
        assert isinstance(editor, QLineEdit)
        editor.setText(index.data(Qt.DisplayRole))

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex) -> None:
        assert isinstance(editor, QLineEdit)
        model.setData(index, editor.text(), Qt.DisplayRole)
