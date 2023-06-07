from enum import Enum
from typing import Dict

from PySide6.QtCore import QObject, Signal, Slot, Qt
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtWidgets import QWidget

from ui.main_window.card_tables.input import InputCardsTableView
from ui.main_window.card_tables.overview import OverviewCardsTableView
from ui.main_window.controllers.deck_controller import DeckController
from ui.main_window.main_window import MainWindow


class ShortcutCommand(Enum):
    SUBMIT_AND_RESET = 1
    SUBMIT_AND_CONTINUE = 2
    REMOVE_LINE = 3
    RESET_INPUT = 4
    ONLINE_LOOKUP = 5


class _ShortcutListener(QObject):
    activated = Signal(ShortcutCommand)

    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.shortcuts: Dict[ShortcutCommand, QShortcut] = {
            ShortcutCommand.SUBMIT_AND_RESET: QShortcut(QKeySequence(Qt.CTRL | Qt.Key_Return), parent),
            ShortcutCommand.SUBMIT_AND_CONTINUE: QShortcut(QKeySequence(Qt.SHIFT | Qt.Key_Return), parent),
            ShortcutCommand.REMOVE_LINE: QShortcut(QKeySequence(Qt.CTRL | Qt.Key_Delete), parent),
            ShortcutCommand.RESET_INPUT: QShortcut(QKeySequence(Qt.CTRL | Qt.Key_Backspace), parent),
            ShortcutCommand.ONLINE_LOOKUP: QShortcut(QKeySequence(Qt.CTRL | Qt.Key_Space), parent),
        }
        for command, shortcut in self.shortcuts.items():
            shortcut.setContext(Qt.WindowShortcut)
            shortcut.activated.connect(lambda shortcut_command=command: self.activated.emit(shortcut_command))


class ShortcutsController(QObject):
    def __init__(self, parent: QObject, main_window: MainWindow, deck_controller: DeckController):
        super().__init__(parent)
        self.deck_controller = deck_controller
        self.shortcut_listener = _ShortcutListener(main_window)
        self.shortcut_listener.activated.connect(self._on_shortcut_activated)

    @Slot(ShortcutCommand)
    def _on_shortcut_activated(self, shortcut_command: ShortcutCommand):
        if self.deck_controller.table_in_focus(InputCardsTableView):
            match shortcut_command:
                case ShortcutCommand.SUBMIT_AND_RESET:
                    self.deck_controller.add_line_to_overview()
                    self.deck_controller.remove_line()
                case ShortcutCommand.SUBMIT_AND_CONTINUE:
                    self.deck_controller.add_line_to_overview()
        elif self.deck_controller.table_in_focus(OverviewCardsTableView):
            match shortcut_command:
                case ShortcutCommand.SUBMIT_AND_RESET:
                    self.deck_controller.reset_input()
                    self.deck_controller.add_line_to_input()
                    self.deck_controller.remove_line()
                    self.deck_controller.focus_input()
                case ShortcutCommand.SUBMIT_AND_CONTINUE:
                    self.deck_controller.reset_input()
                    self.deck_controller.add_line_to_input()
                    self.deck_controller.focus_input()

        if self.deck_controller.table_in_focus():
            match shortcut_command:
                case ShortcutCommand.REMOVE_LINE:
                    self.deck_controller.remove_line()
                case ShortcutCommand.RESET_INPUT:
                    self.deck_controller.reset_input()
                    self.deck_controller.focus_input()
                case ShortcutCommand.ONLINE_LOOKUP:
                    self.deck_controller.lookup_online()
