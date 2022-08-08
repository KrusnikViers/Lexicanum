import sys

from PySide2.QtCore import Slot
from PySide2.QtWidgets import QMainWindow

from app.data.language import Language
from app.wrappers import dictionary as Dictionary
from app.prompts import prompts as Prompts
from app.info import PROJECT_FULL_NAME
from ui.card_input import CardInput, construct_input_from_card, construct_default_input
from ui.gen.main_window_uic import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(PROJECT_FULL_NAME)
        window_width = self.geometry().width()
        self.ui.splitter.setSizes([window_width, window_width])

        default_input = construct_default_input(self)
        self.ui.prompts_layout.insertWidget(0, default_input)

        self.ui.language_to_learn.clicked.connect(self._selected_language_to_learn)
        self.ui.language_answer.clicked.connect(self._selected_language_answer)
        self.ui.reset_variants.clicked.connect(self._reset_prompts)
        self.ui.lookup.clicked.connect(self._lookup)

    @Slot()
    def _lookup(self):
        if not self.ui.source_input.text():
            return

        self._reset_prompts()
        lookup_text = self.ui.source_input.text().strip()
        language = Language.EN if self.ui.language_answer.isChecked() else Language.DE

        dictionary_response = Dictionary.get_raw_translations_list(lookup_text, language)
        cards_list = Prompts.construct_cards_from_dictionary_response(language, dictionary_response)

        # Cards list is reversed, because inserted widgets will be pushing previously inserted down, and first card
        # should end up on top.
        for card in reversed(cards_list):
            card_widget = construct_input_from_card(self.ui.prompts_widget, card)
            self.ui.prompts_layout.insertWidget(1, card_widget)

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

    def closeEvent(self, _) -> None:
        sys.exit(0)
