from typing import List

from PySide6.QtCore import QModelIndex
from PySide6.QtWidgets import QTableView, QWidget, QHeaderView

from ui.cards_table.model.abstract import CardsModelHeader, AbstractCardsModel
from ui.shared.shortcuts import ShortcutCommand


class AbstractCardsTableView(QTableView):
    def __init__(self, parent: QWidget, model: AbstractCardsModel):
        super(AbstractCardsTableView, self).__init__(parent)

        self.setEditTriggers(self.EditTrigger.AllEditTriggers)
        self.setModel(model)

        self.verticalHeader().setVisible(False)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.verticalHeader().setDefaultSectionSize(16)

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
        return [self.horizontalHeader().sectionSize(header.value) for header in CardsModelHeader]

    def set_header_sizes(self, sizes: List[int]):
        for index, size in enumerate(sizes):
            self.horizontalHeader().resizeSection(index, size)

    def execute_shortcut_action(self, shortcut_command: ShortcutCommand):
        index = self.focused_index()
        if index is None:
            return
        self.commit_open_editor_changes()
        assert isinstance(self.model(), AbstractCardsModel)
        self.model().execute_shortcut_action(index.row(), shortcut_command)
