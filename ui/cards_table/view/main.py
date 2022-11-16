from PySide6.QtCore import QModelIndex, Signal
from PySide6.QtWidgets import QWidget, QHeaderView

from app.data import Status
from ui.cards_table.delegate import CardTypeDelegate, LineEditSimpleDelegate
from ui.cards_table.model.base import CardsModelHeader
from ui.cards_table.model.main import MainCardsModel
from ui.cards_table.view.base import BaseCardsTableView
from ui.shared.shortcuts import ShortcutCommand


class MainCardsTableView(BaseCardsTableView):
    lookup_done = Signal()

    def __init__(self, parent: QWidget, main_model: MainCardsModel):
        super(MainCardsTableView, self).__init__(parent, main_model)
        self.main_model = main_model

        self.setItemDelegateForColumn(CardsModelHeader.Type.value, CardTypeDelegate.instance)
        self.setItemDelegateForColumn(CardsModelHeader.Note.value, LineEditSimpleDelegate.instance)
        self.setItemDelegateForColumn(CardsModelHeader.Question.value, LineEditSimpleDelegate.instance)
        self.setItemDelegateForColumn(CardsModelHeader.Answer.value, LineEditSimpleDelegate.instance)

        self.horizontalHeader().setVisible(False)
        self.horizontalHeader().setSectionResizeMode(CardsModelHeader.Type.value, QHeaderView.ResizeMode.Fixed)
        self.horizontalHeader().setSectionResizeMode(CardsModelHeader.Question.value, QHeaderView.ResizeMode.Fixed)
        self.horizontalHeader().setSectionResizeMode(CardsModelHeader.Answer.value, QHeaderView.ResizeMode.Fixed)
        self.horizontalHeader().setSectionResizeMode(CardsModelHeader.Note.value, QHeaderView.ResizeMode.Stretch)

    def maybe_execute_shortcut(self, shortcut_command: ShortcutCommand) -> Status:
        index: QModelIndex | None = self.focused_index()
        model: MainCardsModel = self.model()
        if index is None:
            return Status.no_error()
        if shortcut_command == ShortcutCommand.CLEAR:
            return model.remove_card(index.row())
