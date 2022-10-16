from PySide6.QtCore import QModelIndex, Qt
from PySide6.QtWidgets import QTableView, QWidget, QHeaderView, QAbstractItemDelegate

from app.data.language import Language
from app.translation_lookup.lookup import LookupData
from ui.cards_table.delegate import CardTypeDelegate, LineEditSimpleDelegate, LineEditLookupDelegate
from ui.cards_table.model.abstract import CardsModelHeader, AbstractCardsModel
from ui.shared.shortcuts import ShortcutCommand


class CardsTableView(QTableView):
    def __init__(self, parent: QWidget, model: AbstractCardsModel):
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

    def active_lookup_data(self) -> LookupData | None:
        if index := self._selected_valid_index():
            if CardsModelHeader.of(index.column()) in (CardsModelHeader.Answer, CardsModelHeader.Question):
                # TODO: Move elsewhere
                language = Language.EN if CardsModelHeader.of(
                    index.column()) == CardsModelHeader.Answer else Language.DE
                self._apply_open_editor_changes()
                return LookupData(self.model().data(index, Qt.DisplayRole), language)
        return None

    def _apply_open_editor_changes(self):
        if index := self._selected_valid_index():
            self.commitData(self.indexWidget(index))

    def shortcut_action(self, shortcut_command: ShortcutCommand):
        row = self._selected_row()
        if row is None:
            return
        self._apply_open_editor_changes()
        model: AbstractCardsModel = self.model()
        model.shortcut_action(row, shortcut_command)
