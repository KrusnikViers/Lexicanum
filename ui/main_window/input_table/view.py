from PySide6.QtCore import QModelIndex, Qt, Signal
from PySide6.QtWidgets import QWidget, QHeaderView, QSizePolicy, QComboBox

from core.settings import Settings, StoredSettings
from core.types import Card
from core.util import Status
from ui.common import ShortcutCommand
from ui.common.cards_table import CardsTableView, CardsTableHeader
from ui.common.cards_table.delegates import ComboBoxCardTypeDelegate, LineEditLookupDelegate, LineEditSimpleDelegate
from ui.main_window.input_table.model import InputCardsTableModel


class InputCardsTableView(CardsTableView):
    new_card = Signal(Card)

    def __init__(self, parent: QWidget, input_model: InputCardsTableModel):
        super(InputCardsTableView, self).__init__(parent, input_model)
        self.input_model = input_model

        self.setItemDelegateForColumn(CardsTableHeader.Type.value, ComboBoxCardTypeDelegate.instance)
        self.setItemDelegateForColumn(CardsTableHeader.Question.value, LineEditLookupDelegate.instance)
        self.setItemDelegateForColumn(CardsTableHeader.Answer.value, LineEditLookupDelegate.instance)
        self.setItemDelegateForColumn(CardsTableHeader.Note.value, LineEditSimpleDelegate.instance)

        self.horizontalHeader().setSectionResizeMode(CardsTableHeader.Type.value, QHeaderView.ResizeMode.Fixed)
        self.horizontalHeader().setSectionResizeMode(CardsTableHeader.Question.value,
                                                     QHeaderView.ResizeMode.Interactive)
        self.horizontalHeader().setSectionResizeMode(CardsTableHeader.Answer.value, QHeaderView.ResizeMode.Interactive)
        self.horizontalHeader().setSectionResizeMode(CardsTableHeader.Note.value, QHeaderView.ResizeMode.Stretch)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(self.horizontalHeader().height() + self.verticalHeader().defaultSectionSize())
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def maybe_execute_shortcut(self, shortcut_command: ShortcutCommand) -> Status:
        index: QModelIndex | None = self.focused_index()
        if index is None:
            return Status()
        self.commit_open_editor_changes()
        if shortcut_command == ShortcutCommand.CLEAR:
            self.input_model.reset_data()
        elif shortcut_command == ShortcutCommand.SUGGEST:
            # TODO: Implement
            pass
        elif shortcut_command in (ShortcutCommand.ENTER, ShortcutCommand.ENTER_AND_CONTINUE):
            input_card = self.input_model.get_input_card()
            if not input_card.is_valid():
                return Status('Card is not valid')
            self.new_card.emit(input_card)
            if shortcut_command == ShortcutCommand.ENTER:
                self.input_model.reset_data()
        return Status()

    def store_geometry(self):
        sizes_serialized = ' '.join(map(str, self.header_sizes()))
        Settings.set(StoredSettings.SUMMARY_TABLE_COLUMNS_WIDTH_SPACED, sizes_serialized)

    def restore_geometry(self):
        sizes_packed = Settings.get(StoredSettings.SUMMARY_TABLE_COLUMNS_WIDTH_SPACED)
        sizes = [] if len(sizes_packed) == 0 else [int(size) for size in sizes_packed.split(' ')]
        if len(sizes) != len(CardsTableHeader):
            print('Table geometry invalid: {}, restoring default'.format(sizes))
            sizes = [0, 250, 250, 0]
            assert len(sizes) == len(CardsTableHeader)

        # Always recalculate first column width.
        example_card_type_editor: QComboBox = ComboBoxCardTypeDelegate.instance.createEditor(
            None, None, self.model().index(0, 0, QModelIndex()))
        sizes[CardsTableHeader.Type.value] = example_card_type_editor.minimumSizeHint().width() + 20
        example_card_type_editor.deleteLater()

        self.set_header_sizes(sizes)
