from enum import Enum
from typing import Dict

from PySide6.QtCore import QObject, Slot, Signal, Qt
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtWidgets import QWidget


class ShortcutCommand(Enum):
    ENTER_AND_CONTINUE = 1
    ENTER = 2
    CLEAR = 3
    SUGGEST = 4


class Shortcuts(QObject):
    activated = Signal(ShortcutCommand)

    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.shortcuts: Dict[ShortcutCommand, QShortcut] = {
            ShortcutCommand.ENTER_AND_CONTINUE: QShortcut(QKeySequence(Qt.SHIFT | Qt.Key_Return), parent),
            ShortcutCommand.ENTER: QShortcut(QKeySequence(Qt.CTRL | Qt.Key_Return), parent),
            ShortcutCommand.CLEAR: QShortcut(QKeySequence(Qt.CTRL | Qt.Key_Delete), parent),
            ShortcutCommand.SUGGEST: QShortcut(QKeySequence(Qt.CTRL | Qt.Key_Space), parent),
        }
        for shortcut in self.shortcuts.values():
            shortcut.setContext(Qt.WindowShortcut)
            shortcut.activated.connect(self._shortcut_activated)

    @Slot()
    def _shortcut_activated(self):
        sender: QShortcut = self.sender()
        for key, value in self.shortcuts.items():
            if value == sender:
                self.activated.emit(key)
