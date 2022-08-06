import sys

from PySide2.QtCore import Slot
from PySide2.QtWidgets import QMainWindow

from core.card import Language
from core.dictionary_api import request_translations
from core.dictionary_prompts import get_possible_cards_for
from core.project_info import PROJECT_FULL_NAME
from ui.card_variant import CardVariant
from ui.gen.main_window_uic import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(PROJECT_FULL_NAME)
        window_width = self.geometry().width()
        self.ui.splitter.setSizes([window_width, window_width])

        custom_variant = CardVariant(self)
        custom_variant.disable_drop()
        self.ui.prompts_layout.insertWidget(0, custom_variant)

        self.ui.language_to_learn.clicked.connect(self.selected_language_to_learn)
        self.ui.language_answer.clicked.connect(self.selected_language_answer)
        self.ui.reset_variants.clicked.connect(self.reset_prompts)
        self.ui.lookup.clicked.connect(self.lookup)

    @Slot()
    def lookup(self):
        self.reset_prompts()
        if not self.ui.source_input.text():
            return

        lookup_text = self.ui.source_input.text()
        language = Language.EN if self.ui.language_answer.isChecked() else Language.DE

        dictionary_response = request_translations(lookup_text, language)
        cards = get_possible_cards_for(language, dictionary_response)

        # Cards list is reversed, because inserted widgets will be pushing previously inserted down, and first card
        # should end up on top.
        for card in reversed(cards):
            card_widget = CardVariant(self.ui.prompts_widget, card.card_type, card.question, card.answer, card.note)
            self.ui.prompts_layout.insertWidget(1, card_widget)

    @Slot()
    def reset_prompts(self):
        for child in self.ui.prompts_widget.children():
            if not isinstance(child, CardVariant):
                continue
            if child.ui.drop.isEnabled():
                child.deleteLater()

    @Slot()
    def selected_language_to_learn(self):
        self.ui.language_to_learn.setChecked(True)
        self.ui.language_answer.setChecked(False)

    @Slot()
    def selected_language_answer(self):
        self.ui.language_answer.setChecked(True)
        self.ui.language_to_learn.setChecked(False)

    def closeEvent(self, _) -> None:
        sys.exit(0)
