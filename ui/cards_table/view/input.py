from PySide6.QtCore import QModelIndex, Qt, Signal
from PySide6.QtWidgets import QWidget, QHeaderView, QSizePolicy, QComboBox

from app.data import Settings, StoredSettings, Status
from ui.cards_table.delegate import CardTypeDelegate, LineEditSimpleDelegate, LineEditLookupDelegate
from ui.cards_table.model.base import BaseCardsModel
from ui.cards_table.model.base import CardsModelHeader
from ui.cards_table.model.input import InputCardsModel
from ui.cards_table.view.base import BaseCardsTableView
from ui.shared.shortcuts import ShortcutCommand


class InputCardsTableView(BaseCardsTableView):
    lookup_request = Signal(CardsModelHeader, str)

    def __init__(self, parent: QWidget, input_model: InputCardsModel, main_model: BaseCardsModel):
        super(InputCardsTableView, self).__init__(parent, input_model)
        self.input_model = input_model
        self.main_model = main_model

        self.setItemDelegateForColumn(CardsModelHeader.Type.value, CardTypeDelegate.instance)
        self.setItemDelegateForColumn(CardsModelHeader.Note.value, LineEditSimpleDelegate.instance)
        self.setItemDelegateForColumn(CardsModelHeader.Question.value, LineEditLookupDelegate.instance)
        self.setItemDelegateForColumn(CardsModelHeader.Answer.value, LineEditLookupDelegate.instance)

        self.horizontalHeader().setSectionResizeMode(CardsModelHeader.Type.value, QHeaderView.ResizeMode.Fixed)
        self.horizontalHeader().setSectionResizeMode(CardsModelHeader.Question.value,
                                                     QHeaderView.ResizeMode.Interactive)
        self.horizontalHeader().setSectionResizeMode(CardsModelHeader.Answer.value, QHeaderView.ResizeMode.Interactive)
        self.horizontalHeader().setSectionResizeMode(CardsModelHeader.Note.value, QHeaderView.ResizeMode.Stretch)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(self.horizontalHeader().height() + self.verticalHeader().defaultSectionSize())
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def maybe_execute_shortcut(self, shortcut_command: ShortcutCommand) -> Status:
        index: QModelIndex | None = self.focused_index()
        if index is None:
            return Status.no_error()
        self.commit_open_editor_changes()
        match shortcut_command:
            case ShortcutCommand.SUGGEST:
                if index.column() in (CardsModelHeader.Question.value, CardsModelHeader.Answer.value):
                    self.lookup_request.emit(CardsModelHeader.of(index), self.model().data(index, Qt.DisplayRole))
                else:
                    return Status.from_status('Lookup available only for Question and Answer fields')
            case ShortcutCommand.ENTER_AND_CONTINUE:
                return self.main_model.add_card(self.input_model.get_input_card())
            case ShortcutCommand.ENTER:
                status_result = self.main_model.add_card(self.input_model.get_input_card())
                if status_result.is_ok():
                    self.input_model.reset_data()
                return status_result
            case ShortcutCommand.CLEAR:
                self.input_model.reset_data()
        return Status.no_error()

    def store_geometry(self):
        sizes_serialized = ' '.join(map(str, self.header_sizes()))
        Settings.set(StoredSettings.SUMMARY_TABLE_COLUMNS_WIDTH_SPACED, sizes_serialized)

    def restore_geometry(self):
        sizes_packed = Settings.get(StoredSettings.SUMMARY_TABLE_COLUMNS_WIDTH_SPACED)
        sizes = [] if len(sizes_packed) == 0 else [int(size) for size in sizes_packed.split(' ')]
        if len(sizes) != len(CardsModelHeader):
            print('Table geometry invalid: {}, restoring default'.format(sizes))
            sizes = [0, 250, 250, 0]
            assert len(sizes) == len(CardsModelHeader)

        # Always recalculate first column width.
        example_card_type_editor: QComboBox = CardTypeDelegate.instance.createEditor(
            None, None, self.model().index(0, 0, QModelIndex()))
        sizes[CardsModelHeader.Type.value] = example_card_type_editor.minimumSizeHint().width() + 20
        example_card_type_editor.deleteLater()

        self.set_header_sizes(sizes)
