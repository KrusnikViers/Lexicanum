from PySide6.QtCore import Slot, QModelIndex
from PySide6.QtWidgets import QTableView, QWidget, QHeaderView

from ui.cards_table_model import CardsTableModel, CardsModelHeaders
from ui.cards_table_subwidgets import CardTypeDelegate, CardPlainStringDelegate, CardActButton
from ui.line_edit_with_lookup import CardLineEditWithLookupDelegate


class CardsTableView(QTableView):
    def __init__(self, parent: QWidget, model: CardsTableModel):
        super(CardsTableView, self).__init__(parent)

        self.setEditTriggers(self.AllEditTriggers)
        self.setModel(model)
        self.delegate_card_type = CardTypeDelegate()
        self.setItemDelegateForColumn(
            CardsModelHeaders.Type.value, self.delegate_card_type)
        self.delegate_plain_string = CardPlainStringDelegate()
        self.setItemDelegateForColumn(
            CardsModelHeaders.Note.value, self.delegate_plain_string)
        self.delegate_string_lookup = CardLineEditWithLookupDelegate()
        self.setItemDelegateForColumn(
            CardsModelHeaders.Question.value, self.delegate_string_lookup)
        self.setItemDelegateForColumn(
            CardsModelHeaders.Answer.value, self.delegate_string_lookup)

        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.verticalHeader().setDefaultSectionSize(16)
        self.horizontalHeader().setSectionResizeMode(CardsModelHeaders.Type.value, QHeaderView.Fixed)
        self.horizontalHeader().resizeSection(CardsModelHeaders.Type.value, 120)
        self.horizontalHeader().setSectionResizeMode(CardsModelHeaders.Question.value, QHeaderView.Interactive)
        self.horizontalHeader().resizeSection(CardsModelHeaders.Question.value, 200)
        self.horizontalHeader().setSectionResizeMode(CardsModelHeaders.Answer.value, QHeaderView.Interactive)
        self.horizontalHeader().resizeSection(CardsModelHeaders.Answer.value, 200)
        self.horizontalHeader().setSectionResizeMode(CardsModelHeaders.Note.value, QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(CardsModelHeaders.Act.value, QHeaderView.Fixed)
        self.horizontalHeader().resizeSection(CardsModelHeaders.Act.value, 16)

        for row in range(0, self.model().rowCount()):
            self._update_act(row)

    def _update_act(self, row: int):
        index = self.model().index(row, CardsModelHeaders.Act.value)
        if not isinstance(self.indexWidget(index), CardActButton):
            new_widget = CardActButton(self, row)
            new_widget.clicked.connect(self._act_button_pressed)
            self.setIndexWidget(index, new_widget)

    @Slot()
    def _act_button_pressed(self):
        sender: CardActButton = self.sender()
        model: CardsTableModel = self.model()
        model.act_on_row(sender.row_number)

    @Slot()
    def rowsInserted(self, parent: QModelIndex, start: int, end: int) -> None:
        # |end| is inclusive
        for row in range(start, end + 1):
            self._update_act(row)
