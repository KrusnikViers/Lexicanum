from PySide6.QtCore import QModelIndex, Signal
from PySide6.QtWidgets import QWidget, QHeaderView

from core.types import Card
from core.util import Status
from ui.common import ShortcutCommand
from ui.common.cards_table import ComboBoxCardTypeDelegate, LineEditSimpleDelegate, CardsTableView, CardsTableHeader
from ui.lookup_dialog.suggestions_table.model import SuggestionCardsTableModel


class SuggestionCardsTableView(CardsTableView):
    suggestion_accepted = Signal(Card)
    # TODO: Support in dialog
    done = Signal()

    def __init__(self, parent: QWidget, suggestions_model: SuggestionCardsTableModel):
        super().__init__(parent, suggestions_model)
        self.suggestions_model = suggestions_model

        # Delegates
        self.setItemDelegateForColumn(CardsTableHeader.Type.value, ComboBoxCardTypeDelegate.instance)
        self.setItemDelegateForColumn(CardsTableHeader.Note.value, LineEditSimpleDelegate.instance)
        self.setItemDelegateForColumn(CardsTableHeader.Question.value, LineEditSimpleDelegate.instance)
        self.setItemDelegateForColumn(CardsTableHeader.Answer.value, LineEditSimpleDelegate.instance)

        # Default geometry
        self.horizontalHeader().setVisible(False)
        self.horizontalHeader().setSectionResizeMode(CardsTableHeader.Type.value, QHeaderView.ResizeMode.Fixed)
        self.horizontalHeader().setSectionResizeMode(CardsTableHeader.Question.value, QHeaderView.ResizeMode.Fixed)
        self.horizontalHeader().setSectionResizeMode(CardsTableHeader.Answer.value, QHeaderView.ResizeMode.Fixed)
        self.horizontalHeader().setSectionResizeMode(CardsTableHeader.Note.value, QHeaderView.ResizeMode.Stretch)

    def maybe_execute_shortcut(self, shortcut_command: ShortcutCommand) -> Status:
        # TODO: Implement
        index: QModelIndex | None = self.focused_index()
        return Status.no_error()
