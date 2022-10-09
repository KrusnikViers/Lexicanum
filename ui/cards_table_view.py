from PySide6.QtCore import QModelIndex
from PySide6.QtWidgets import QTableView, QWidget, QHeaderView, QAbstractItemDelegate

from ui.cards_model.generic import CardsModelHeader, GenericCardsModel
from ui.shortcuts import ShortcutCommand
from ui.subwidgets import CardTypeDelegate, LineEditSimpleDelegate, LineEditLookupDelegate


class CardsTableView(QTableView):
    def __init__(self, parent: QWidget, model: GenericCardsModel):
        super(CardsTableView, self).__init__(parent)

        self.setEditTriggers(self.AllEditTriggers)
        self.setModel(model)
        self.card_type_delegate = CardTypeDelegate()
        self.setItemDelegateForColumn(
            CardsModelHeader.Type.value, self.card_type_delegate)
        self.line_edit_simple_delegate = LineEditSimpleDelegate()
        self.setItemDelegateForColumn(
            CardsModelHeader.Note.value, self.line_edit_simple_delegate)
        self.line_edit_lookup_delegate = LineEditLookupDelegate()
        self.setItemDelegateForColumn(
            CardsModelHeader.Question.value, self.line_edit_lookup_delegate)
        self.setItemDelegateForColumn(
            CardsModelHeader.Answer.value, self.line_edit_lookup_delegate)

        self.current_editor: QAbstractItemDelegate | None = None

        # TODO: Make proper resizing behaviour
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.verticalHeader().setDefaultSectionSize(16)
        self.horizontalHeader().setSectionResizeMode(CardsModelHeader.Type.value, QHeaderView.Fixed)
        self.horizontalHeader().resizeSection(CardsModelHeader.Type.value, 120)
        self.horizontalHeader().setSectionResizeMode(CardsModelHeader.Question.value, QHeaderView.Interactive)
        self.horizontalHeader().resizeSection(CardsModelHeader.Question.value, 250)
        self.horizontalHeader().setSectionResizeMode(CardsModelHeader.Answer.value, QHeaderView.Interactive)
        self.horizontalHeader().resizeSection(CardsModelHeader.Answer.value, 250)
        self.horizontalHeader().setSectionResizeMode(CardsModelHeader.Note.value, QHeaderView.Stretch)

    def _selected_valid_index(self) -> QModelIndex | None:
        current_index = self.currentIndex()
        if current_index.isValid() and self.indexWidget(current_index).hasFocus():
            return current_index
        return None

    def _selected_row(self) -> int | None:
        if index := self._selected_valid_index():
            return index.row()
        return None

    def _apply_open_editor_changes(self):
        if index := self._selected_valid_index():
            self.commitData(self.indexWidget(index))

    def shortcut_action(self, shortcut_command: ShortcutCommand):
        row = self._selected_row()
        if row is None:
            return
        self._apply_open_editor_changes()
        model: GenericCardsModel = self.model()
        model.shortcut_action(row, shortcut_command)
