import sys

from PySide2.QtCore import Slot, Qt, QDateTime
from PySide2.QtWidgets import QFileDialog
from PySide2.QtWidgets import QMainWindow, QTableWidgetItem

from app.data.card import Card
from app.data.language import Language
from app.data.storage.csv import CSVWrapper
from app.info import PROJECT_FULL_NAME
from app.info import PROJECT_NAME
from app.prompts import prompts
from app.wrappers import dictionary
from ui.card_input import CardInput, construct_input_from_card, construct_default_input
from ui.gen.main_window_uic import Ui_MainWindow


class MainWindow(QMainWindow):
    # Fields, stored alongside cards in the table but not displayed to the user.
    _TABLE_TYPE_ROLE = Qt.UserRole + 1
    _TABLE_ID_ROLE = Qt.UserRole + 2

    def __init__(self):
        super(MainWindow, self).__init__()

        # General UI settings
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(PROJECT_FULL_NAME)
        window_width = self.geometry().width()
        self.ui.splitter.setSizes([window_width, window_width])

        # Table settings
        table_width = window_width / 2
        self.ui.deck_table.setColumnWidth(0, table_width * 0.15)  # Type
        self.ui.deck_table.setColumnWidth(1, table_width * 0.30)  # Question
        self.ui.deck_table.setColumnWidth(2, table_width * 0.30)  # Answer
        self._deck_changed()
        CSVWrapper.register_dialect()

        # Card prompts settings
        default_input = construct_default_input(self)
        default_input.accepted.connect(self._prompt_accepted)
        self.ui.prompts_layout.insertWidget(0, default_input)

        # Built-in signals
        self.ui.source_input.returnPressed.connect(self.ui.lookup.click)

        # Custom signals
        self.ui.language_to_learn.clicked.connect(self._selected_language_to_learn)
        self.ui.language_answer.clicked.connect(self._selected_language_answer)
        self.ui.reset_variants.clicked.connect(self._reset_prompts)
        self.ui.lookup.clicked.connect(self._lookup)
        self.ui.export_deck.clicked.connect(self._export_deck)
        self.ui.import_deck.clicked.connect(self._import_deck)

    @Slot()
    def _lookup(self):
        if not self.ui.source_input.text():
            return

        self._reset_prompts()
        lookup_text = self.ui.source_input.text().strip()
        language = Language.EN if self.ui.language_answer.isChecked() else Language.DE

        dictionary_response = dictionary.get_raw_translations_list(lookup_text, language)
        cards_list = prompts.construct_cards_from_dictionary_response(language, dictionary_response)

        # Cards list is reversed, because inserted widgets will be pushing previously inserted down, and first card
        # should end up on top.
        for card in reversed(cards_list):
            card_widget = construct_input_from_card(self.ui.prompts_widget, card)
            card_widget.accepted.connect(self._prompt_accepted)
            self.ui.prompts_layout.insertWidget(1, card_widget)

    @Slot()
    def _prompt_accepted(self):
        sender: CardInput = self.sender()
        assert isinstance(sender, CardInput)
        self._add_card(sender.get_as_card())

    def _card_from_row(self, row_index: int) -> Card:
        assert row_index < self.ui.deck_table.rowCount()
        return Card(self.ui.deck_table.item(row_index, 0).data(self._TABLE_TYPE_ROLE),
                    self.ui.deck_table.item(row_index, 1).text(),
                    self.ui.deck_table.item(row_index, 2).text(),
                    self.ui.deck_table.item(row_index, 3).text(),
                    self.ui.deck_table.item(row_index, 0).data(self._TABLE_ID_ROLE))

    def _add_card(self, card: Card):
        self.ui.deck_table.insertRow(0)

        # Type column is rather special: it holds all card metadata (hidden) and can not be edited in place.
        type_item = QTableWidgetItem(card.card_type.name)
        type_item.setData(self._TABLE_TYPE_ROLE, card.card_type)
        type_item.setData(self._TABLE_ID_ROLE, QDateTime.currentMSecsSinceEpoch())
        type_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        type_item.setTextAlignment(Qt.AlignCenter)
        self.ui.deck_table.setItem(0, 0, type_item)

        self.ui.deck_table.setItem(0, 1, QTableWidgetItem(card.question))
        self.ui.deck_table.setItem(0, 2, QTableWidgetItem(card.answer))
        self.ui.deck_table.setItem(0, 3, QTableWidgetItem(card.note))

    @Slot()
    def _reset_prompts(self):
        for child in self.ui.prompts_widget.children():
            if not isinstance(child, CardInput):
                continue
            if child.is_prompt:
                child.deleteLater()

    @Slot()
    def _selected_language_to_learn(self):
        self.ui.language_to_learn.setChecked(True)
        self.ui.language_answer.setChecked(False)

    @Slot()
    def _selected_language_answer(self):
        self.ui.language_answer.setChecked(True)
        self.ui.language_to_learn.setChecked(False)

    @Slot()
    def _deck_changed(self):
        pass
        # self.ui.export_deck.setEnabled(self.ui.deck_table.rowCount() > 0)

    @Slot()
    def _export_deck(self):
        # TODO: Add project directory caching
        file_search_result = QFileDialog.getSaveFileName(self, "Save {} & Anki files...".format(PROJECT_NAME),
                                                         filter="Text tables (*.csv)")
        if not file_search_result[0]:
            return
        deck = [self._card_from_row(row_index) for row_index in range(0, self.ui.deck_table.rowCount())]
        csv_wrapper = CSVWrapper(file_search_result[0])
        csv_wrapper.export_deck(deck)

    @Slot()
    def _import_deck(self):
        file_search_result = QFileDialog.getOpenFileNames(self, "Open {} .csv file...".format(PROJECT_NAME),
                                                          filter="Text tables (*.csv)")
        if not file_search_result[0]:
            return

        while self.ui.deck_table.rowCount() > 0:
            self.ui.deck_table.removeRow(0)
        csv_wrapper = CSVWrapper(file_search_result[0][0])
        deck = csv_wrapper.import_deck()
        for card in deck:
            self._add_card(card)

    def closeEvent(self, _) -> None:
        sys.exit(0)
