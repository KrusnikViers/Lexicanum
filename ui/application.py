import sys

from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QApplication

from core.types.deck import Deck
from lookup.wiktionary.interface import WiktionaryInterface
from ui.main_window.controllers.deck_controller import DeckController
from ui.main_window.controllers.file_controller import FileController
from ui.main_window.controllers.shortcuts_controller import ShortcutsController
from ui.main_window.main_window import MainWindow


class Application(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.Floor)

        startup_deck = FileController.startup_deck()

        self.main_window = MainWindow(startup_deck)
        self.main_window.application_exit_requested.connect(self.on_exit_requested)

        self.lookup_interface = WiktionaryInterface()
        self.deck_controller = DeckController(self, self.main_window, self.lookup_interface, startup_deck)
        self.shortcuts_controller = ShortcutsController(self, self.main_window, self.deck_controller)
        self.file_controller = FileController(self, self.main_window, self.deck_controller)

    @Slot()
    def on_exit_requested(self):
        self.main_window.application_closing = True
        self.main_window.close()
        self.quit()
