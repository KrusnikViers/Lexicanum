import sys
from pathlib import Path

from PySide2.QtCore import Slot, Qt, QDateTime
from PySide2.QtWidgets import QFileDialog, QApplication, QMainWindow, QTableWidgetItem

from app.data.card import Card
from app.data.deck import Deck
from app.data.language import Language
from app.data.storage.anki import AnkiWriter
from app.data.storage.deck_json import DeckJsonWriter
from app.data.storage.settings import Settings, StoredSettings
from app.info import PROJECT_NAME, PROJECT_FULL_NAME
from app.prompts import prompts
from app.wrappers import dictionary
from ui.card_input import CardInput
from ui.gen.main_window_uic import Ui_MainWindow

_TABLE_TYPE_ROLE = Qt.UserRole + 1
_TABLE_ID_ROLE = Qt.UserRole + 2

_TABLE_TYPE_INDEX = 0
_TABLE_QUESTION_INDEX = 1
_TABLE_ANSWER_INDEX = 2
_TABLE_NOTE_INDEX = 3


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(PROJECT_FULL_NAME)
        # Disable "help" button on the top panel - context prompts are not supported.
        QApplication.instance().setAttribute(Qt.AA_DisableWindowContextHelpButton)
        self._init_window_geometry()

        self._init_word_lookup()
        self._init_prompts()
        self._init_deck()
        self.show()

    def _init_window_geometry(self):
        window_width = self.geometry().width()
        self.ui.splitter.setSizes([window_width, window_width])

    def _init_word_lookup(self):
        self.ui.word_input.returnPressed.connect(self.ui.word_lookup.click)
        self.ui.word_language_question.clicked.connect(self._word_language_change)
        self.ui.word_language_answer.clicked.connect(self._word_language_change)
        self.ui.word_lookup.clicked.connect(self._word_lookup)

    def _init_prompts(self):
        self.default_prompt = CardInput.create_default(self)
        self.default_prompt.accepted.connect(self._prompt_accepted)
        self.ui.prompts_layout.insertWidget(0, self.default_prompt)
        self.ui.prompts_reset.clicked.connect(self._prompts_reset)

    def _init_deck(self):
        self.ui.deck_import_on_startup.setChecked(Settings.get(StoredSettings.IMPORT_ON_STARTUP))
        self.ui.deck_import_on_startup.stateChanged.connect(self._deck_import_on_startup_changed)
        if Settings.get(StoredSettings.IMPORT_ON_STARTUP):
            self._deck_import_from_file(Settings.get(StoredSettings.LAST_IMPORT_PATH))

        self.ui.deck_export.clicked.connect(self._deck_export)
        self.ui.deck_import.clicked.connect(self._deck_import)

        table_width = self.geometry().width() / 2
        self.ui.deck_cards_table.setColumnWidth(_TABLE_TYPE_INDEX, table_width * 0.15)
        self.ui.deck_cards_table.setColumnWidth(_TABLE_QUESTION_INDEX, table_width * 0.30)
        self.ui.deck_cards_table.setColumnWidth(_TABLE_ANSWER_INDEX, table_width * 0.30)

    @Slot()
    def _word_lookup(self):
        if not self.ui.word_input.text():
            self.ui.word_input.setStyleSheet("border: 1px solid red")
            return
        self.ui.word_input.setStyleSheet('')

        self._prompts_reset()
        lookup_text = self.ui.word_input.text().strip()
        language = Language.EN if self.ui.word_language_answer.isChecked() else Language.DE

        dictionary_response = dictionary.get_raw_translations_list(lookup_text, language)
        cards_list = prompts.construct_cards_from_dictionary_response(language, dictionary_response)
        # Cards list is reversed, because inserted widgets will be pushing previously inserted down, and first card
        # should end up on top.
        for card in reversed(cards_list):
            card_widget = CardInput(self, card.card_type, card.question, card.answer, card.note)
            card_widget.accepted.connect(self._prompt_accepted)
            self.ui.prompts_layout.insertWidget(1, card_widget)

    @Slot()
    def _prompt_accepted(self):
        sender: CardInput = self.sender()
        assert isinstance(sender, CardInput)
        self._add_card_to_top(sender.get_as_card())
        # Non-default prompt can be removed after that
        sender.maybe_close()

    def _card_from_row(self, row_index: int) -> Card:
        assert row_index < self.ui.deck_cards_table.rowCount()
        return Card(card_type=self.ui.deck_cards_table.item(row_index, _TABLE_TYPE_INDEX).data(_TABLE_TYPE_ROLE),
                    question=self.ui.deck_cards_table.item(row_index, _TABLE_QUESTION_INDEX).text().strip(),
                    answer=self.ui.deck_cards_table.item(row_index, _TABLE_ANSWER_INDEX).text().strip(),
                    note=self.ui.deck_cards_table.item(row_index, _TABLE_NOTE_INDEX).text().strip(),
                    card_id=self.ui.deck_cards_table.item(row_index, _TABLE_TYPE_INDEX).data(_TABLE_ID_ROLE))

    def _add_card_to_top(self, card: Card):
        self.ui.deck_cards_table.insertRow(0)

        # Type column is rather special: it holds all card metadata (hidden) and can not be edited in place.
        type_item = QTableWidgetItem(card.card_type.name)
        type_item.setData(_TABLE_TYPE_ROLE, card.card_type)
        type_item.setData(_TABLE_ID_ROLE, QDateTime.currentMSecsSinceEpoch())
        type_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        type_item.setTextAlignment(Qt.AlignCenter)
        self.ui.deck_cards_table.setItem(0, _TABLE_TYPE_INDEX, type_item)

        self.ui.deck_cards_table.setItem(0, _TABLE_QUESTION_INDEX, QTableWidgetItem(card.question))
        self.ui.deck_cards_table.setItem(0, _TABLE_ANSWER_INDEX, QTableWidgetItem(card.answer))
        self.ui.deck_cards_table.setItem(0, _TABLE_NOTE_INDEX, QTableWidgetItem(card.note))

    @Slot()
    def _prompts_reset(self):
        for child in self.ui.prompts_widget.children():
            if not isinstance(child, CardInput):
                continue
            child.maybe_drop()

    @Slot()
    def _word_language_change(self):
        self.ui.word_language_question.setChecked(self.sender() == self.ui.word_language_question)
        self.ui.word_language_answer.setChecked(self.sender() == self.ui.word_language_answer)

    @Slot()
    def _deck_export(self):
        file_search_result = QFileDialog.getSaveFileName(self, "Save {} & Anki files...".format(PROJECT_NAME),
                                                         dir=Settings.get(StoredSettings.LAST_EXPORT_PATH),
                                                         filter="Deck JSON (*.json)")
        if not file_search_result[0]:
            return
        Settings.set(StoredSettings.LAST_EXPORT_PATH, file_search_result[0])

        cards = [self._card_from_row(row_index) for row_index in range(0, self.ui.deck_cards_table.rowCount())]
        deck = Deck(deck_name=self.ui.deck_name.text().strip(), cards=cards)
        deck.normalize_for_output()

        output_path = Path(file_search_result[0]).resolve()
        DeckJsonWriter.write_to_file(deck, output_path.with_suffix('.json'))
        AnkiWriter.write_to_file(deck, output_path.with_suffix('.apkg'))

    @Slot()
    def _deck_import_on_startup_changed(self):
        Settings.set(StoredSettings.IMPORT_ON_STARTUP, self.ui.deck_import_on_startup.isChecked())

    @Slot()
    def _deck_import(self):
        file_search_result = QFileDialog.getOpenFileName(self, "Open {} .json file...".format(PROJECT_NAME),
                                                         dir=Settings.get(StoredSettings.LAST_IMPORT_PATH),
                                                         filter="Deck JSON (*.json)")
        if not file_search_result[0]:
            return
        Settings.set(StoredSettings.LAST_IMPORT_PATH, file_search_result[0])

        while self.ui.deck_cards_table.rowCount() > 0:
            self.ui.deck_cards_table.removeRow(0)
        self._deck_import_from_file(file_search_result[0])

    def _deck_import_from_file(self, file_name: str):
        input_path = Path(file_name)
        deck = DeckJsonWriter.read_from_file(input_path.resolve().with_suffix('.json'))
        if deck is None:
            return
        self.ui.deck_name.setText(deck.deck_name)
        for card in deck.cards:
            self._add_card_to_top(card)

    def closeEvent(self, _) -> None:
        sys.exit(0)
