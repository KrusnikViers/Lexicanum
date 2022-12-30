from PySide6.QtCore import QModelIndex
from PySide6.QtWidgets import QWidget, QHeaderView

from core.util import Status
from ui.common import ShortcutCommand
from ui.common.cards_table import CardsTableView, CardsTableHeader
from ui.common.cards_table.delegates import ComboBoxCardTypeDelegate, LineEditSimpleDelegate
from ui.main_window.overview_table.model import OverviewCardsTableModel


class OverviewCardsTableView(CardsTableView):
    def __init__(self, parent: QWidget, overview_model: OverviewCardsTableModel):
        super(OverviewCardsTableView, self).__init__(parent, overview_model)
        self.overview_model = overview_model

        self.setItemDelegateForColumn(CardsTableHeader.Type.value, ComboBoxCardTypeDelegate.instance)
        self.setItemDelegateForColumn(CardsTableHeader.Note.value, LineEditSimpleDelegate.instance)
        self.setItemDelegateForColumn(CardsTableHeader.Question.value, LineEditSimpleDelegate.instance)
        self.setItemDelegateForColumn(CardsTableHeader.Answer.value, LineEditSimpleDelegate.instance)

        self.horizontalHeader().setVisible(False)
        self.horizontalHeader().setSectionResizeMode(CardsTableHeader.Type.value, QHeaderView.ResizeMode.Fixed)
        self.horizontalHeader().setSectionResizeMode(CardsTableHeader.Question.value, QHeaderView.ResizeMode.Fixed)
        self.horizontalHeader().setSectionResizeMode(CardsTableHeader.Answer.value, QHeaderView.ResizeMode.Fixed)
        self.horizontalHeader().setSectionResizeMode(CardsTableHeader.Note.value, QHeaderView.ResizeMode.Stretch)

    def maybe_execute_shortcut(self, shortcut_command: ShortcutCommand) -> Status:
        index: QModelIndex | None = self.focused_index()
        if index is None:
            return Status()
        if shortcut_command == ShortcutCommand.CLEAR:
            return self.overview_model.remove_card(index)
        return Status()
