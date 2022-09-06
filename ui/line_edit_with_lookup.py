from PySide2.QtCore import QModelIndex, QAbstractItemModel, Qt
from PySide2.QtWidgets import QStyledItemDelegate, QWidget, QStyleOptionViewItem

from ui.gen.line_edit_with_lookup_uic import Ui_LineEditWithLookup
from ui.icons.icons import SharedIcons


class CardLineEditWithLookupDelegate(QStyledItemDelegate):
    class Widget(QWidget):
        def __init__(self, parent: QWidget):
            super(CardLineEditWithLookupDelegate.Widget, self).__init__(parent)
            self.ui = Ui_LineEditWithLookup()
            self.ui.setupUi(self)
            self.ui.lookup.setIcon(SharedIcons.Search)

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> QWidget:
        return self.Widget(parent)

    def setEditorData(self, editor: QWidget, index: QModelIndex) -> None:
        assert isinstance(editor, self.Widget)
        editor.ui.line_edit.setText(index.data(Qt.DisplayRole))

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex) -> None:
        assert isinstance(editor, self.Widget)
        model.setData(index, editor.ui.line_edit.text(), Qt.DisplayRole)
