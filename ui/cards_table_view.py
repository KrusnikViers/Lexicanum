from PySide2.QtCore import Slot, QModelIndex
from PySide2.QtWidgets import QTableView, QWidget

from ui.cards_table_model import CardsTableModel
from ui.cards_table_subwidgets import CardTypeDelegate, CardPlainStringDelegate, CardActButton
from ui.line_edit_with_lookup import CardLineEditWithLookupDelegate


class CardsTableView(QTableView):
    def __init__(self, parent: QWidget, model: CardsTableModel):
        super(CardsTableView, self).__init__(parent)

        self.setEditTriggers(self.AllEditTriggers)
        self.setModel(model)
        self.delegate_card_type = CardTypeDelegate()
        self.setItemDelegateForColumn(
            CardsTableModel.Headers.Type.value, self.delegate_card_type)
        self.delegate_plain_string = CardPlainStringDelegate()
        self.setItemDelegateForColumn(
            CardsTableModel.Headers.Note.value, self.delegate_plain_string)
        self.delegate_string_lookup = CardLineEditWithLookupDelegate()
        self.setItemDelegateForColumn(
            CardsTableModel.Headers.Question.value, self.delegate_string_lookup)
        self.setItemDelegateForColumn(
            CardsTableModel.Headers.Answer.value, self.delegate_string_lookup)

        for row in range(0, self.model().rowCount()):
            self._update_act(row)

    def _update_act(self, row: int):
        index = self.model().index(row, CardsTableModel.Headers.Act.value)
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
