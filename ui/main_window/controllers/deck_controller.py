from enum import Enum
from typing import Dict

from PySide6.QtCore import QObject, Slot, Signal, Qt
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtWidgets import QWidget

from ui.main_window.main_window import MainWindow


class _ShortcutCommand(Enum):
    SUBMIT_AND_RESET = 1
    SUBMIT_AND_CONTINUE = 2
    CLEAR_AND_RESET = 3
    CLEAR_AND_CONTINUE = 4
    SEARCH_IN_DICTIONARY = 5
    # SEARCH_IN_DECK = 6


class _ShortcutListener(QObject):
    activated = Signal(_ShortcutCommand)

    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.shortcuts: Dict[_ShortcutCommand, QShortcut] = {
            _ShortcutCommand.SUBMIT_AND_RESET: QShortcut(QKeySequence(Qt.CTRL | Qt.Key_Return), parent),
            _ShortcutCommand.SUBMIT_AND_CONTINUE: QShortcut(QKeySequence(Qt.SHIFT | Qt.Key_Return), parent),
            _ShortcutCommand.CLEAR_AND_RESET: QShortcut(QKeySequence(Qt.CTRL | Qt.Key_Delete), parent),
            _ShortcutCommand.CLEAR_AND_CONTINUE: QShortcut(QKeySequence(Qt.SHIFT | Qt.Key_Delete), parent),
            _ShortcutCommand.SEARCH_IN_DICTIONARY: QShortcut(QKeySequence(Qt.CTRL | Qt.Key_Space), parent),
            # TODO(viers): Support for Beta
            # _ShortcutCommand.SEARCH_IN_DECK: QShortcut(QKeySequence(Qt.CONTROL | Qt.Key_F), parent),
        }
        for shortcut in self.shortcuts.values():
            shortcut.setContext(Qt.WindowShortcut)
            shortcut.activated.connect(self._shortcut_activated)

    @Slot()
    def _shortcut_activated(self):
        sender: QShortcut = self.sender()
        # TODO(viers): Rewrite
        for key, value in self.shortcuts.items():
            if value == sender:
                self.activated.emit(key)


class DeckController(QObject):
    def __init__(self, parent: QObject, main_window: MainWindow):
        super().__init__(parent)
        self.ui = main_window
        self.shortcut_listener = _ShortcutListener(main_window)
