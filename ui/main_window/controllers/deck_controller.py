from copy import deepcopy
from typing import Type

from PySide6.QtCore import QObject, Slot

from core.types import Deck
from lookup.interface import LookupInterface
from ui.main_window.card_tables.base import CardsTableView, CardsTableHeader, CardsTableModel
from ui.main_window.card_tables.input import InputCardsTableView
from ui.main_window.main_window import MainWindow


class DeckController(QObject):
    def __init__(self, parent: QObject, main_window: MainWindow, lookup_interface: LookupInterface,
                 starting_deck: Deck):
        super().__init__(parent)
        self.main_window = main_window
        self.lookup_interface = lookup_interface

        self.deck = starting_deck
        self.reset_deck(starting_deck)
        assert self.deck is self.main_window.overview_model.deck

        self.main_window.ui.deck_info_title_input.textEdited.connect(self.on_deck_name_changed)

    def table_in_focus(self, expected_type: Type[CardsTableView] | None = None) -> CardsTableView | None:
        focused_widget = self.main_window.focusWidget()
        while focused_widget and not isinstance(focused_widget, CardsTableView):
            focused_widget = focused_widget.parentWidget()
        if isinstance(focused_widget, CardsTableView) and (
                expected_type is None or isinstance(focused_widget, expected_type)):
            return focused_widget
        return None

    @staticmethod
    def default_deck():
        return Deck('New Deck', [])

    @Slot(str)
    def on_deck_name_changed(self, new_name: str):
        self.deck.deck_name = new_name

    def update_deck_meta(self):
        self.main_window.ui.deck_info_title_input.setText(self.deck.deck_name)
        path_label_text = str(self.deck.file_path) if self.deck.file_path else 'Not saved anywhere'
        self.main_window.ui.deck_info_path_label.setText(path_label_text)

    def reset_deck(self, new_deck: Deck):
        self.deck = deepcopy(new_deck)
        self.main_window.overview_model.reset_deck(self.deck)
        self.update_deck_meta()

    # Submits current row, if valid, from input table to the overview. If card is not valid, shows error message in
    # status bar. Input table must be in focus.
    def submit_from_input(self):
        assert self.table_in_focus(InputCardsTableView)
        selection = self.main_window.input_table_view.selected_index()
        if not selection:
            return
        selected_card = self.main_window.input_model.get_card(selection.row())
        validity = selected_card.validity_status()
        if not validity:
            self.main_window.status_bar.show_timed_message(validity.status)
            return
        self.main_window.overview_model.insert_card(deepcopy(selected_card))

    # Removes current line from either input or overview table. If it is the last line in input, just clears its
    # content. One of the tables should be in focus.
    def remove_line(self):
        assert self.table_in_focus()
        focused_table_view = self.table_in_focus()
        selection = focused_table_view.selected_index()
        if not selection:
            return
        model: CardsTableModel = focused_table_view.model()
        model.remove_card(selection)
        # Focused table may lose focus on this action, reinstate it in this case.
        focused_table_view.setFocus()

    # Resets input table. No previous focus requirements.
    def reset_input(self):
        self.main_window.input_model.reset_content()

    # Sets focus to the first cell of input. No previous focus requirements.
    def focus_input(self):
        self.main_window.input_table_view.setFocus()

    # Looks up word from question or answer from either input or overview table. Results of the lookup replace
    # existing content of the input. One of the tables should be in focus.
    def lookup_online(self):
        table_in_focus = self.table_in_focus()
        assert table_in_focus

        lookup_index = table_in_focus.focused_index()
        if not lookup_index:
            self.main_window.status_bar.show_timed_message('No cell selected with word to search')
            return
        if lookup_index.column() not in [CardsTableHeader.Answer.value, CardsTableHeader.Question.value]:
            self.main_window.status_bar.show_timed_message('Selection is not in Question or Answer column')
            return

        table_in_focus.commit_open_editor_changes()
        original_card = table_in_focus.model().get_card(lookup_index.row())
        is_lookup_from_answer = lookup_index.column() == CardsTableHeader.Answer.value
        search_string = original_card.answer.strip() if is_lookup_from_answer else original_card.question.strip()
        if search_string == '':
            self.main_window.status_bar.show_timed_message('Selected cell is empty')
            return

        lookup_status = self.lookup_interface.lookup_by_answer(search_string) if is_lookup_from_answer \
            else self.lookup_interface.lookup_by_question(search_string)
        if not lookup_status.is_ok():
            self.main_window.status_bar.show_timed_message(lookup_status.status)
            return

        self.main_window.input_model.reset_content(lookup_status.value)
