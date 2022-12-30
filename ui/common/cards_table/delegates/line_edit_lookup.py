from PySide6.QtCore import QModelIndex, QAbstractItemModel, Qt, Signal
from PySide6.QtWidgets import QStyledItemDelegate, QWidget, QStyleOptionViewItem

from ui.common.icons.list import IconsList
from ui.gen.common.cards_table.delegates.line_edit_lookup_uic import Ui_LineEditLookupDelegate


class _LineEditLookupDelegateWidget(QWidget):
    data_changed = Signal()

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.ui = Ui_LineEditLookupDelegate()
        self.ui.setupUi(self)
        self.ui.lookup.setIcon(IconsList.Search)
        self.ui.line_edit.textChanged.connect(self.data_changed)
        self.setFocusProxy(self.ui.line_edit)


# TODO: Handle 'lookup' button pressed as well
class LineEditLookupDelegate(QStyledItemDelegate):
    instance = None

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> QWidget:
        editor = _LineEditLookupDelegateWidget(parent)
        editor.data_changed.connect(lambda created_editor=editor: self.commitData.emit(created_editor))
        return editor

    def setEditorData(self, editor: _LineEditLookupDelegateWidget, index: QModelIndex) -> None:
        editor.ui.line_edit.setText(index.data(Qt.DisplayRole))

    def setModelData(self, editor: _LineEditLookupDelegateWidget,
                     model: QAbstractItemModel, index: QModelIndex) -> None:
        model.setData(index, editor.ui.line_edit.text(), Qt.DisplayRole)


LineEditLookupDelegate.instance = \
    LineEditLookupDelegate() if LineEditLookupDelegate.instance is None else LineEditLookupDelegate.instance
