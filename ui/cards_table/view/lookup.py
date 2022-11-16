from PySide6.QtCore import QModelIndex, Signal
from PySide6.QtWidgets import QWidget, QHeaderView

from app.data import Status
from ui.cards_table.delegate import CardTypeDelegate, LineEditSimpleDelegate
from ui.cards_table.model.base import CardsModelHeader, BaseCardsModel
from ui.cards_table.model.lookup import LookupCardsModel
from ui.cards_table.view.base import BaseCardsTableView
from ui.shared.shortcuts import ShortcutCommand


class LookupCardsTableView(BaseCardsTableView):
    lookup_done = Signal()

    def __init__(self, parent: QWidget, lookup_model: LookupCardsModel, main_model: BaseCardsModel):
        super(LookupCardsTableView, self).__init__(parent, lookup_model)
        self.lookup_model = lookup_model
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
        if index is None:
            return Status.no_error()
        self.commit_open_editor_changes()
        match shortcut_command:
            case ShortcutCommand.ENTER_AND_CONTINUE:
                return self.main_model.add_card(self.lookup_model.get_card(index.row()))
            case ShortcutCommand.ENTER:
                status_result = self.main_model.add_card(self.lookup_model.get_card(index.row()))
                if status_result.is_ok():
                    self.lookup_done.emit()
                return status_result
            case ShortcutCommand.CLEAR:
                self.lookup_model.remove_card(index.row())
        return Status.no_error()
