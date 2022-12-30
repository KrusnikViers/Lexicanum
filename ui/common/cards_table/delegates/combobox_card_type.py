from PySide6.QtCore import QModelIndex, Qt, Slot
from PySide6.QtWidgets import QStyledItemDelegate, QWidget, QStyleOptionViewItem, QComboBox

from core.types import CardType
from ui.common.cards_table.model import CardsTableModel


class ComboBoxCardTypeDelegate(QStyledItemDelegate):
    instance = None

    @staticmethod
    def _typed_values(editor, model) -> (QComboBox, CardsTableModel):
        assert isinstance(editor, QComboBox)
        assert isinstance(model, CardsTableModel)
        return editor, model

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> QWidget:
        editor, model = self._typed_values(QComboBox(parent), index.model())

        for card_type in CardType:
            if card_type == CardType.Invalid:
                if model.supports_invalid_card_type():
                    editor.addItem(CardType.Invalid.display_name(), userData=CardType.Invalid)
                    editor.insertSeparator(len(CardType))
                continue
            editor.addItem(card_type.display_name(), userData=card_type)

        # TODO: Connect directly?
        editor.currentIndexChanged.connect(self.on_selection_changed)
        return editor

    def setEditorData(self, raw_editor, index: QModelIndex) -> None:
        editor, model = self._typed_values(raw_editor, index.model())

        type_to_choose = model.get_card(index.row()).card_type
        for selection_index in range(0, editor.count()):
            if editor.itemData(selection_index, role=Qt.UserRole) == type_to_choose:
                editor.setCurrentIndex(selection_index)
                break

    def setModelData(self, editor: QComboBox, model: CardsTableModel, index: QModelIndex) -> None:
        model.setData(index, editor.currentData(Qt.UserRole), Qt.DisplayRole)

    @Slot()
    def on_selection_changed(self):
        self.commitData.emit(self.sender())


ComboBoxCardTypeDelegate.instance = \
    ComboBoxCardTypeDelegate() if ComboBoxCardTypeDelegate.instance is None else ComboBoxCardTypeDelegate.instance
