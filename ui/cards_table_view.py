from PySide2.QtWidgets import QTableView, QWidget, QPushButton

from ui.cards_table_delegates import CardTypeDelegate, CardPlainStringDelegate
from ui.cards_table_model import CardsTableModel
from ui.icons.icons import SharedIcons
from ui.line_edit_with_lookup import CardLineEditWithLookupDelegate


class CardsTableView(QTableView):
    def __init__(self, parent: QWidget, model: CardsTableModel):
        super(CardsTableView, self).__init__(parent)

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
        for i in range(0, self.model().rowCount()):
            self.setIndexWidget(
                self.model().index(i, CardsTableModel.Headers.Act.value),
                QPushButton(SharedIcons.Plus if i == 0 else SharedIcons.Trash, '', self))
