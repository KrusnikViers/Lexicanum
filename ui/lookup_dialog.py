from typing import List

from PySide6.QtCore import Qt, QRect, QModelIndex, Slot
from PySide6.QtWidgets import QDialog, QMainWindow

from ui.cards_table.model.lookup import LookupCardsModel
from ui.cards_table.view import CardsTableView
from ui.gen.lookup_dialog_uic import Ui_LookupDialog
from ui.shared.shortcuts import Shortcuts, ShortcutCommand


class LookupDialog(QDialog):
    def __init__(self, parent: QMainWindow, lookup_model: LookupCardsModel):
        super(LookupDialog, self).__init__(parent)

        self.ui = Ui_LookupDialog()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setModal(True)

        self.shortcuts = Shortcuts(self)
        self.shortcuts.activated.connect(self.on_shortcut_activated)

        self.table_model = lookup_model
        self.table_view = CardsTableView(self, self.table_model)
        self.ui.main_layout.replaceWidget(self.ui.table_view_placeholder, self.table_view)
        self.ui.table_view_placeholder.setParent(None)
        self.ui.table_view_placeholder.deleteLater()
        self.table_view.horizontalHeader().setVisible(False)

        self.show()

    def adjust_to_row(self, row_rect: QRect, column_sizes: List[int]):
        # Row height for the lookup view should be the same one as for the main view.
        window_geometry = self.parent().geometry()
        dialog_geometry = self.geometry()
        view_geometry = self.table_view.geometry()

        dialog_top = row_rect.bottom() + window_geometry.top()
        # No need to adjust for viewport, as headers are hidden. Last 4px are for rounding headroom on HiDPI displays.
        desired_table_view_height = self.table_model.rowCount(QModelIndex()) * row_rect.height() + 2
        dialog_height = desired_table_view_height + dialog_geometry.height() - view_geometry.height()
        dialog_left = window_geometry.left() + row_rect.left() - view_geometry.left()
        dialog_width = row_rect.width() + dialog_geometry.width() - view_geometry.width()
        self.setGeometry(QRect(dialog_left, dialog_top, dialog_width, dialog_height))
        self.table_view.set_header_sizes(column_sizes)

    @Slot(ShortcutCommand)
    def on_shortcut_activated(self, shortcut_command: ShortcutCommand):
        self.table_view.execute_shortcut_action(shortcut_command)
        if shortcut_command == ShortcutCommand.ENTER:
            self.accept()
