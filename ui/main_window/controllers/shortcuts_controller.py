from enum import Enum
from typing import Dict, Type

from PySide6.QtCore import QObject, Signal, Slot, Qt
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtWidgets import QWidget

from ui.main_window.card_tables.base import CardsTableView
from ui.main_window.card_tables.input import InputCardsTableView
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
    def __init__(self, parent: QObject, main_window: MainWindow):
        super().__init__(parent)
        self.ui = main_window
        self.shortcut_listener = _ShortcutListener(main_window)
        self.shortcut_listener.activated.connect(self._on_shortcut_activated)

    def table_in_focus(self, expected_type: Type[CardsTableView] | None = None) -> CardsTableView | None:
        focused_widget = self.ui.focusWidget()
        if isinstance(focused_widget, CardsTableView) and (
                expected_type is None or isinstance(focused_widget, expected_type)):
            return focused_widget
        return None

    @Slot(ShortcutCommand)
    def _on_shortcut_activated(self, shortcut_command: ShortcutCommand):
        print(shortcut_command)
        if shortcut_command == ShortcutCommand.SUBMIT_AND_RESET and self.table_in_focus(InputCardsTableView):
            self.submit_from_input()
            self.reset_input()
        elif shortcut_command == ShortcutCommand.SUBMIT_AND_CONTINUE and self.table_in_focus(InputCardsTableView):
            self.submit_from_input()
        elif shortcut_command == ShortcutCommand.REMOVE_LINE and self.table_in_focus():
            self.remove_line()
        elif shortcut_command == ShortcutCommand.RESET_INPUT:
            self.reset_input()
        elif shortcut_command == ShortcutCommand.ONLINE_LOOKUP and self.table_in_focus():
            self.lookup_online()

    # Submits current row, if valid, from input table to the overview. If card is not valid, shows error message in
    # status bar. Input table must be in focus.
    def submit_from_input(self):
        assert self.table_in_focus(InputCardsTableView)
        pass

    # Removes current line from either input or overview table. If it is the last line in input, just clears its
    # content. One of the tables should be in focus.
    def remove_line(self):
        assert self.table_in_focus()
        pass

    # Resets input table and sets focus in the first cell of it. No previous focus requirements, as long as window is
    # active.
    def reset_input(self):
        pass

    # Looks up word from question or answer from either input or overview table. Results of the lookup replace
    # existing content of the input. One of the tables should be in focus.
    def lookup_online(self):
        assert self.table_in_focus()
        pass
