from PySide6.QtCore import QModelIndex, QAbstractItemModel, Qt
from PySide6.QtWidgets import QStyledItemDelegate, QWidget, QStyleOptionViewItem

from ui.gen.subwidgets.line_edit_lookup_delegate_uic import Ui_LineEditLookupDelegate
from ui.icons.icons import SharedIcons


class LineEditLookupDelegate(QStyledItemDelegate):
    class Widget(QWidget):
        def __init__(self, parent: QWidget):
            super(LineEditLookupDelegate.Widget, self).__init__(parent)
            self.ui = Ui_LineEditLookupDelegate()
            self.ui.setupUi(self)
            self.ui.lookup.setIcon(SharedIcons.Search)
            self.setFocusProxy(self.ui.line_edit)

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> QWidget:
        return self.Widget(parent)

    def setEditorData(self, editor: QWidget, index: QModelIndex) -> None:
        assert isinstance(editor, self.Widget)
        editor.ui.line_edit.setText(index.data(Qt.DisplayRole))

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex) -> None:
        assert isinstance(editor, self.Widget)
        model.setData(index, editor.ui.line_edit.text(), Qt.DisplayRole)
