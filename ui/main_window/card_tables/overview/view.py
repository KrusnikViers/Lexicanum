from PySide6.QtWidgets import QWidget, QHeaderView, QSizePolicy

from ui.main_window.card_tables.base import CardsTableView, CardsTableHeader
from ui.main_window.card_tables.delegates import ComboBoxCardTypeDelegate, LineEditSimpleDelegate
from ui.main_window.card_tables.overview.model import OverviewCardsTableModel


class OverviewCardsTableView(CardsTableView):
    def __init__(self, parent: QWidget, overview_model: OverviewCardsTableModel):
        super().__init__(parent, overview_model)
        self.overview_model = overview_model

        self.setItemDelegateForColumn(CardsTableHeader.Type.value, ComboBoxCardTypeDelegate.instance)
        self.setItemDelegateForColumn(CardsTableHeader.Question.value, LineEditSimpleDelegate.instance)
        self.setItemDelegateForColumn(CardsTableHeader.Grammar.value, LineEditSimpleDelegate.instance)
        self.setItemDelegateForColumn(CardsTableHeader.Answer.value, LineEditSimpleDelegate.instance)
        self.setItemDelegateForColumn(CardsTableHeader.Note.value, LineEditSimpleDelegate.instance)

        self.horizontalHeader().setVisible(False)
        self.horizontalHeader().setSectionResizeMode(CardsTableHeader.Type.value, QHeaderView.ResizeMode.Fixed)
        self.horizontalHeader().setSectionResizeMode(CardsTableHeader.Question.value, QHeaderView.ResizeMode.Fixed)
        self.horizontalHeader().setSectionResizeMode(CardsTableHeader.Answer.value, QHeaderView.ResizeMode.Fixed)
        self.horizontalHeader().setSectionResizeMode(CardsTableHeader.Note.value, QHeaderView.ResizeMode.Stretch)

        # Always display at least 10 rows of overview table
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        self.setMinimumHeight(self.verticalHeader().defaultSectionSize() * 10)
