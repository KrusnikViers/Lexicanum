from typing import List

from PySide6.QtCore import QModelIndex
from PySide6.QtWidgets import QTableView, QWidget, QHeaderView

from core.util import Status
from ui.common.cards_table.header import CardsTableHeader
from ui.common.cards_table.model import CardsTableModel
from ui.common.shortcuts import ShortcutCommand


class CardsTableView(QTableView):
    def __init__(self, parent: QWidget, model: CardsTableModel):
        super().__init__(parent)

        self.setEditTriggers(self.EditTrigger.AllEditTriggers)
        self.setModel(model)

        self.verticalHeader().setVisible(False)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.verticalHeader().setDefaultSectionSize(16)

    # Virtual methods
    def maybe_execute_shortcut(self, shortcut_command: ShortcutCommand) -> Status:
        raise NotImplementedError

    # Common methods
    def selected_index(self) -> QModelIndex | None:
        current_index = self.currentIndex()
        if current_index.isValid():
            return current_index
        return None

    def focused_index(self) -> QModelIndex | None:
        selected_index = self.selected_index()
        if selected_index and self.indexWidget(selected_index).hasFocus():
            return selected_index
        return None

    def commit_open_editor_changes(self):
        if index := self.focused_index():
            self.commitData(self.indexWidget(index))

    def header_sizes(self) -> List[int]:
        return [self.horizontalHeader().sectionSize(header.value) for header in CardsTableHeader]

    def set_header_sizes(self, sizes: List[int]):
        for index, size in enumerate(sizes):
            self.horizontalHeader().resizeSection(index, size)
