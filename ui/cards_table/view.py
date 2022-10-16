from typing import List

from PySide6.QtCore import QModelIndex, Qt, QRect
from PySide6.QtWidgets import QTableView, QWidget, QHeaderView, QAbstractItemDelegate

from app.data.language import Language
from app.data.storage.settings import Settings, StoredSettings
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

        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.verticalHeader().setDefaultSectionSize(16)
        self.horizontalHeader().setSectionResizeMode(CardsModelHeader.Type.value, QHeaderView.Fixed)
        self.horizontalHeader().setSectionResizeMode(CardsModelHeader.Question.value, QHeaderView.Interactive)
        self.horizontalHeader().setSectionResizeMode(CardsModelHeader.Answer.value, QHeaderView.Interactive)
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

    def active_row_rect(self) -> QRect:
        if index := self._selected_valid_index():
            view_geometry = self.geometry()
            return QRect(view_geometry.left(),
                         self.rowViewportPosition(index.row()) + view_geometry.top() + self.viewport().geometry().top(),
                         view_geometry.width(), self.rowHeight(index.row()))

    def _apply_open_editor_changes(self):
        if index := self._selected_valid_index():
            self.commitData(self.indexWidget(index))

    def get_header_sizes(self) -> List[int]:
        return [self.horizontalHeader().sectionSize(header.value) for header in CardsModelHeader]

    def set_header_sizes(self, sizes: List[int]):
        for index, size in enumerate(sizes):
            self.horizontalHeader().resizeSection(index, size)

    def restore_geometry(self):
        sizes = [int(size) for size in Settings.get(StoredSettings.SUMMARY_TABLE_COLUMNS_WIDTH_SPACED).split(' ')]
        if len(sizes) != len(CardsModelHeader):
            print('Table geometry invalid: {}, restoring default'.format(sizes))
            sizes = [120, 250, 250, 0]
            assert len(sizes) == len(CardsModelHeader)
        self.set_header_sizes(sizes)

    def store_geometry(self):
        sizes_serialized = ' '.join(map(str, self.get_header_sizes()))
        Settings.set(StoredSettings.SUMMARY_TABLE_COLUMNS_WIDTH_SPACED, sizes_serialized)

    def shortcut_action(self, shortcut_command: ShortcutCommand):
        row = self._selected_row()
        if row is None:
            return
        self._apply_open_editor_changes()
        model: AbstractCardsModel = self.model()
        model.shortcut_action(row, shortcut_command)
