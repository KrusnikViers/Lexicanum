from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QHeaderView, QSizePolicy

from core.types import Card
from ui.main_window.card_tables.base import CardsTableView, CardsTableHeader
from ui.main_window.card_tables.delegates import ComboBoxCardTypeDelegate, LineEditSimpleDelegate
from ui.main_window.card_tables.input.model import InputCardsTableModel


class InputCardsTableView(CardsTableView):
    new_card = Signal(Card)

    def __init__(self, parent: QWidget, input_model: InputCardsTableModel):
        super().__init__(parent, input_model)
        self.input_model = input_model

        self.setItemDelegateForColumn(CardsTableHeader.Type.value, ComboBoxCardTypeDelegate.instance)
        self.setItemDelegateForColumn(CardsTableHeader.Question.value, LineEditSimpleDelegate.instance)
        self.setItemDelegateForColumn(CardsTableHeader.Grammar.value, LineEditSimpleDelegate.instance)
        self.setItemDelegateForColumn(CardsTableHeader.Answer.value, LineEditSimpleDelegate.instance)
        self.setItemDelegateForColumn(CardsTableHeader.Note.value, LineEditSimpleDelegate.instance)

        self.horizontalHeader().setSectionResizeMode(CardsTableHeader.Type.value, QHeaderView.ResizeMode.Fixed)
        self.horizontalHeader().setSectionResizeMode(CardsTableHeader.Question.value,
                                                     QHeaderView.ResizeMode.Interactive)
        self.horizontalHeader().setSectionResizeMode(CardsTableHeader.Answer.value, QHeaderView.ResizeMode.Interactive)
        self.horizontalHeader().setSectionResizeMode(CardsTableHeader.Note.value, QHeaderView.ResizeMode.Stretch)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        self.setMaximumHeight(self.horizontalHeader().height() + self.verticalHeader().defaultSectionSize())
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
