from copy import deepcopy
from typing import Type

from PySide6.QtCore import QObject

from ui.main_window.card_tables.base import CardsTableView
from ui.main_window.card_tables.input import InputCardsTableView
from ui.main_window.main_window import MainWindow


class DeckController(QObject):
    def __init__(self, parent: QObject, main_window: MainWindow):
        super().__init__(parent)
        self.ui = main_window

    def table_in_focus(self, expected_type: Type[CardsTableView] | None = None) -> CardsTableView | None:
        focused_widget = self.ui.focusWidget()
        while focused_widget and not isinstance(focused_widget, CardsTableView):
            focused_widget = focused_widget.parentWidget()
        if isinstance(focused_widget, CardsTableView) and (
                expected_type is None or isinstance(focused_widget, expected_type)):
            return focused_widget
        return None

    # Submits current row, if valid, from input table to the overview. If card is not valid, shows error message in
    # status bar. Input table must be in focus.
    def submit_from_input(self):
        assert self.table_in_focus(InputCardsTableView)
        selection = self.ui.input_table_view.selected_index()
        if not selection:
            return
        selected_card = self.ui.input_model.get_card(selection.row())
        validity = selected_card.validity_status()
        if not validity:
            self.ui.status_bar.show_timed_message(validity.status)
            return
        self.ui.overview_model.insert_card(deepcopy(selected_card))

    # Removes current line from either input or overview table. If it is the last line in input, just clears its
    # content. One of the tables should be in focus.
    def remove_line(self):
        assert self.table_in_focus()
        pass

    # Resets input table. No previous focus requirements.
    def reset_input(self):
        pass

    # Sets focus to the first cell of input. No previous focus requirements.
    def focus_input(self):
        pass

    # Looks up word from question or answer from either input or overview table. Results of the lookup replace
    # existing content of the input. One of the tables should be in focus.
    def lookup_online(self):
        assert self.table_in_focus()
        pass
