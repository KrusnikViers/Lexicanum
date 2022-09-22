from PySide6.QtCore import Slot, QModelIndex
from PySide6.QtWidgets import QTableView, QWidget, QHeaderView, QAbstractItemView, QAbstractItemDelegate

from ui.cards_table_model import CardsTableModel, CardsModelHeaders
from ui.cards_table_subwidgets import CardTypeDelegate, CardPlainStringDelegate, CardActButton
from ui.line_edit_with_lookup import CardLineEditWithLookupDelegate
from ui.shortcuts import ShortcutCommand


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

        self.current_editor: QAbstractItemDelegate | None = None

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

    def _selected_row(self) -> int | None:
        current_index = self.currentIndex()
        if current_index.row() != -1 and \
                self.state() == QAbstractItemView.EditingState and \
                self.indexWidget(current_index).hasFocus():
            return self.currentIndex().row()
        return None

    def _apply_open_editor_changes(self):
        if self.state() == QAbstractItemView.EditingState:
            self.commitData(self.indexWidget(self.currentIndex()))

    def shortcut_action(self, shortcut_command: ShortcutCommand):
        row = self._selected_row()
        model: CardsTableModel = self.model()
        if row is None:
            return
        self._apply_open_editor_changes()
        if row == 0 and shortcut_command in (ShortcutCommand.ENTER, ShortcutCommand.ENTER_AND_CONTINUE):
            model.new_row_from_stub()
        if row == 0 and shortcut_command in (ShortcutCommand.ENTER, ShortcutCommand.CLEAR):
            model.clean_stub_data()
        if row != 0 and shortcut_command == ShortcutCommand.CLEAR:
            model.remove_row(row)

    @Slot()
    def _act_button_pressed(self):
        sender: CardActButton = self.sender()
        row = sender.row_number
        model: CardsTableModel = self.model()
        if row == 0:
            self._apply_open_editor_changes()
            model.new_row_from_stub()
        else:
            model.remove_row(row)

    @Slot()
    def rowsInserted(self, parent: QModelIndex, start: int, end: int) -> None:
        # |end| is inclusive
        for row in range(start, end + 1):
            self._update_act(row)
