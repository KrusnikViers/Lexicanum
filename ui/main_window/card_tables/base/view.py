from typing import List

from PySide6.QtCore import QModelIndex
from PySide6.QtWidgets import QTableView, QWidget, QHeaderView

from core.settings import Settings, StoredSettings
from ui.main_window.card_tables.base.header import CardsTableHeader
from ui.main_window.card_tables.base.model import CardsTableModel
from ui.main_window.card_tables.delegates import ComboBoxCardTypeDelegate


class CardsTableView(QTableView):
    def __init__(self, parent: QWidget, model: CardsTableModel):
        super().__init__(parent)

        self.setEditTriggers(self.EditTrigger.AllEditTriggers)
        self.setModel(model)

        self.verticalHeader().setVisible(False)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.verticalHeader().setDefaultSectionSize(16)

    # Common methods
    def is_in_focus(self) -> bool:
        return self.hasFocus()

    def selected_index(self) -> QModelIndex | None:
        current_index = self.currentIndex()
        if current_index.isValid():
            return current_index
        return None

    def focused_index(self) -> QModelIndex | None:
        if not self.is_in_focus():
            return None
        selected_index = self.selected_index()
        if selected_index and self.indexWidget(selected_index).hasFocus():
            return selected_index
        return None

    def commit_open_editor_changes(self):
        if index := self.focused_index():
            self.commitData(self.indexWidget(index))

    def get_header_sizes(self) -> List[int]:
        return [self.horizontalHeader().sectionSize(header.value) for header in CardsTableHeader]

    def set_header_sizes(self, sizes: List[int]):
        for index, size in enumerate(sizes):
            self.horizontalHeader().resizeSection(index, size)

    def store_headers_geometry(self):
        sizes_serialized = ' '.join(map(str, self.get_header_sizes()))
        Settings.set(StoredSettings.CARDS_TABLE_COLUMNS_WIDTH_SPACED, sizes_serialized)

    def restore_headers_geometry(self):
        cached_header_geometry = Settings.get(StoredSettings.CARDS_TABLE_COLUMNS_WIDTH_SPACED).split(' ')
        if len(cached_header_geometry) != len(CardsTableHeader):
            cached_header_geometry = [0, 200, 200, 200, 0]
            assert len(cached_header_geometry) == len(CardsTableHeader)

        # Always recalculate first column width.
        cached_header_geometry[CardsTableHeader.Type.value] = ComboBoxCardTypeDelegate.min_editor_width() + 20
        self.set_header_sizes(cached_header_geometry)
