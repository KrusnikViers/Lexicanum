from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QMainWindow

from ui.cards_table.model.lookup import LookupCardsModel
from ui.cards_table.view import CardsTableView
from ui.gen.lookup_dialog_uic import Ui_LookupDialog


class LookupDialog(QDialog):
    def __init__(self, parent: QMainWindow, lookup_model: LookupCardsModel):
        super(LookupDialog, self).__init__(parent)

        self.ui = Ui_LookupDialog()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)

        self.table_model = lookup_model
        self.table_view = CardsTableView(self, self.table_model)
        self.ui.main_layout.replaceWidget(self.ui.table_view_placeholder, self.table_view)
        self.ui.table_view_placeholder.setParent(None)
        self.ui.table_view_placeholder.deleteLater()

        self.show()
