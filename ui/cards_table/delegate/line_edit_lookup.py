from PySide6.QtCore import QModelIndex, QAbstractItemModel, Qt, Slot, Signal
from PySide6.QtWidgets import QStyledItemDelegate, QWidget, QStyleOptionViewItem

from ui.gen.cards_table.delegate.line_edit_lookup_uic import Ui_LineEditLookupDelegate
from ui.shared.icons.icons import SharedIcons


# TODO: Handle 'lookup' button pressed as well
class LineEditLookupDelegate(QStyledItemDelegate):
    instance = None

    class Widget(QWidget):
        data_changed = Signal()

        def __init__(self, parent: QWidget):
            super(LineEditLookupDelegate.Widget, self).__init__(parent)
            self.ui = Ui_LineEditLookupDelegate()
            self.ui.setupUi(self)
            self.ui.lookup.setIcon(SharedIcons.Search)
            self.setFocusProxy(self.ui.line_edit)
            self.ui.line_edit.textChanged.connect(self.data_changed)

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> QWidget:
        editor = self.Widget(parent)
        editor.data_changed.connect(self.on_data_changed)
        return editor

    def setEditorData(self, editor: QWidget, index: QModelIndex) -> None:
        assert isinstance(editor, self.Widget)
        editor.ui.line_edit.setText(index.data(Qt.DisplayRole))

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex) -> None:
        assert isinstance(editor, self.Widget)
        model.setData(index, editor.ui.line_edit.text(), Qt.DisplayRole)

    @Slot()
    def on_data_changed(self):
        self.commitData.emit(self.sender())


LineEditLookupDelegate.instance = \
    LineEditLookupDelegate() if LineEditLookupDelegate.instance is None else LineEditLookupDelegate.instance
