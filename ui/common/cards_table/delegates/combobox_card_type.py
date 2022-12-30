from PySide6.QtCore import QModelIndex, Qt
from PySide6.QtWidgets import QWidget, QStyleOptionViewItem, QStyledItemDelegate, QComboBox

from core.types import CardType
from ui.common.cards_table.model import CardsTableModel


class ComboBoxCardTypeDelegate(QStyledItemDelegate):
    instance = None

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> QWidget:
        editor = QComboBox(parent)
        model: CardsTableModel = index.model()

        for card_type in CardType:
            if card_type == CardType.Invalid:
                if model.supports_invalid_card_type():
                    editor.addItem(CardType.Invalid.display_name(), userData=CardType.Invalid)
                    editor.insertSeparator(len(CardType))
                continue
            editor.addItem(card_type.display_name(), userData=card_type)

        editor.currentIndexChanged.connect(lambda _, created_editor=editor: self.commitData.emit(created_editor))
        return editor

    def setEditorData(self, editor: QComboBox, index: QModelIndex) -> None:
        model: CardsTableModel = index.model()

        type_to_choose = model.get_card(index.row()).card_type
        for selection_index in range(0, editor.count()):
            if editor.itemData(selection_index, role=Qt.UserRole) == type_to_choose:
                editor.setCurrentIndex(selection_index)
                break

    def setModelData(self, editor: QComboBox, model: CardsTableModel, index: QModelIndex) -> None:
        model.setData(index, editor.currentData(Qt.UserRole), Qt.DisplayRole)


ComboBoxCardTypeDelegate.instance = \
    ComboBoxCardTypeDelegate() if ComboBoxCardTypeDelegate.instance is None else ComboBoxCardTypeDelegate.instance
