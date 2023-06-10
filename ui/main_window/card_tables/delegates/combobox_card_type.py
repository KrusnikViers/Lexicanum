from PySide6.QtCore import QModelIndex, Qt
from PySide6.QtWidgets import QWidget, QStyleOptionViewItem, QStyledItemDelegate, QComboBox

from core.types import CardType
from ui.main_window.card_tables.base import CardsTableModel


class ComboBoxCardTypeDelegate(QStyledItemDelegate):
    instance = None

    @classmethod
    def min_editor_width(cls, input_model: CardsTableModel):
        example_card_type_editor: QComboBox = ComboBoxCardTypeDelegate.instance.createEditor(
            None, None, input_model.index(0, 0, QModelIndex()))
        min_width = example_card_type_editor.minimumSizeHint().width()
        example_card_type_editor.deleteLater()
        return min_width

    # Qt methods overload
    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> QWidget:
        editor = QComboBox(parent)
        model: CardsTableModel = index.model()
        assert isinstance(model, CardsTableModel)

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
        card_type = model.get_card(index.row()).card_type
        editor.setCurrentIndex(editor.findData(card_type))

    def setModelData(self, editor: QComboBox, model: CardsTableModel, index: QModelIndex) -> None:
        model.setData(index, editor.currentData(Qt.UserRole), Qt.DisplayRole)


ComboBoxCardTypeDelegate.instance = \
    ComboBoxCardTypeDelegate() if ComboBoxCardTypeDelegate.instance is None else ComboBoxCardTypeDelegate.instance
