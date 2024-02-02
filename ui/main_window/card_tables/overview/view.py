from PySide6.QtWidgets import QWidget, QHeaderView, QSizePolicy

from ui.main_window.card_tables.base import CardsTableView, CardsTableHeader
from ui.main_window.card_tables.delegates import ComboBoxCardTypeDelegate, LineEditSimpleDelegate
from ui.main_window.card_tables.overview.model import OverviewCardsTableModel


class OverviewCardsTableView(CardsTableView):
    def __init__(self, parent: QWidget, overview_model: OverviewCardsTableModel):
        super().__init__(parent, overview_model)
        self.overview_model = overview_model

        self.setItemDelegateForColumn(CardsTableHeader.Type.value, ComboBoxCardTypeDelegate.instance)
        for column_index in range(CardsTableHeader.Question.value, CardsTableHeader.Note.value + 1):
            self.setItemDelegateForColumn(column_index, LineEditSimpleDelegate.instance)

        self.horizontalHeader().setVisible(False)
        for column_index in range(CardsTableHeader.Type.value, CardsTableHeader.Note.value):
            self.horizontalHeader().setSectionResizeMode(column_index, QHeaderView.ResizeMode.Fixed)
        self.horizontalHeader().setSectionResizeMode(CardsTableHeader.Note.value, QHeaderView.ResizeMode.Stretch)

        # Always display at least 10 rows of overview table
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        self.setMinimumHeight(self.verticalHeader().defaultSectionSize() * 10)
