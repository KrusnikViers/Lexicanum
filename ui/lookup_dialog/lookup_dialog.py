from typing import List

from PySide6.QtCore import Qt, QRect, Slot, Signal
from PySide6.QtWidgets import QDialog, QMainWindow

from core.types import Card
from lookup import LookupResponse
from ui.common import Shortcuts, ShortcutCommand
from ui.gen.lookup_dialog.lookup_dialog_uic import Ui_LookupDialog


class LookupDialog(QDialog):
    notification = Signal(str)
    new_card = Signal(Card)

    def __init__(self, parent: QMainWindow, lookup_data: LookupResponse):
        super(LookupDialog, self).__init__(parent)

        self.ui = Ui_LookupDialog()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setModal(True)

        self.shortcuts = Shortcuts(self)
        self.shortcuts.activated.connect(self.on_shortcut_activated)

        # TODO: Implement
        # self.lookup_model = lookup_model
        # self.table_view = LookupCardsTableView(self, lookup_model, main_model)
        # self.ui.main_layout.replaceWidget(self.ui.table_view_placeholder, self.table_view)
        # self.ui.table_view_placeholder.setParent(None)
        # self.ui.table_view_placeholder.deleteLater()
        # self.table_view.lookup_done.connect(self.accept)

        self.show()

    @Slot(ShortcutCommand)
    def on_shortcut_activated(self, shortcut_command: ShortcutCommand):
        # TODO: Implement
        pass
