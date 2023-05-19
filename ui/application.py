import sys

from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QApplication

from core.types.deck import Deck
from ui.main_window.controllers.deck_controller import DeckController
from ui.main_window.main_window import MainWindow


class Application(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.Floor)

        self.main_window = MainWindow(self.get_startup_deck())
        self.main_window.application_exit_requested.connect(self.on_exit_requested)

        self.deck_controller = DeckController(self, self.main_window)

    @staticmethod
    def get_startup_deck():
        return Deck('New Deck', [])

    @Slot()
    def on_exit_requested(self):
        self.main_window.application_closing = True
        self.main_window.close()
        self.quit()
