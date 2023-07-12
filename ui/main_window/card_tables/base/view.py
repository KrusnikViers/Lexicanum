from typing import List

from PySide6.QtCore import QModelIndex
from PySide6.QtWidgets import QTableView, QWidget, QHeaderView

from ui.main_window.card_tables.base.header import CardsTableHeader
from ui.main_window.card_tables.base.model import CardsTableModel


class CardsTableView(QTableView):
    def __init__(self, parent: QWidget, model: CardsTableModel):
        super().__init__(parent)

        self.setEditTriggers(self.EditTrigger.AllEditTriggers)
        self.setModel(model)

        self.horizontalHeader().setMinimumSectionSize(200)

        self.verticalHeader().setVisible(False)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.verticalHeader().setDefaultSectionSize(16)

    # Common methods
    def selected_index(self) -> QModelIndex | None:
        current_index = self.currentIndex()
        if current_index.isValid():
            return current_index
        return None

    def focused_index(self) -> QModelIndex | None:
        selected_index = self.selected_index()
        if selected_index and self.indexWidget(selected_index) and self.indexWidget(selected_index).hasFocus():
            return selected_index
        return None

    def commit_open_editor_changes(self):
        if index := self.focused_index():
            self.commitData(self.indexWidget(index))

    def get_header_sizes(self) -> List[int]:
        return [self.horizontalHeader().sectionSize(header.value) for header in CardsTableHeader]

    def set_header_sizes(self, sizes: List[int]):
        for index, size in enumerate(sizes):
            self.horizontalHeader().resizeSection(index, int(size))
