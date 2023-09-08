from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QWidget, QHeaderView, QSizePolicy, QAbstractScrollArea

from core.settings import Settings, StoredSettings
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
        self.horizontalHeader().setSectionResizeMode(CardsTableHeader.Grammar.value, QHeaderView.ResizeMode.Interactive)
        self.horizontalHeader().setSectionResizeMode(CardsTableHeader.Answer.value, QHeaderView.ResizeMode.Interactive)
        self.horizontalHeader().setSectionResizeMode(CardsTableHeader.Note.value, QHeaderView.ResizeMode.Stretch)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        self.setMaximumHeight(self.horizontalHeader().height() + self.verticalHeader().defaultSectionSize())
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)

        self.input_model.row_count_changed.connect(self.on_row_count_changed)
        self.on_row_count_changed()

    @Slot()
    def on_row_count_changed(self):
        # New widget height can not be more than half of parent widget.
        max_height = self.parent().height() // 2

        # First row always present and must always be visible.
        min_height = self.horizontalHeader().height() + self.rowHeight(0) + 2  # Smh +2 saves the day
        if self.horizontalScrollBar().isVisible():
            min_height += self.horizontalScrollBar().height()
        self.setMinimumHeight(min_height)

        # Try to show all the rows, but do now take more space than that.
        extra_rows_height = 0
        for row in range(1, self.verticalHeader().count()):
            extra_rows_height += self.rowHeight(row)
        self.setMaximumHeight(min(max_height, min_height + extra_rows_height))

    def store_headers_geometry(self):
        sizes_serialized = ' '.join(map(str, self.get_header_sizes()))
        Settings.set(StoredSettings.CARDS_TABLE_COLUMNS_WIDTH_SPACED, sizes_serialized)

    def restore_headers_geometry(self):
        cached_header_geometry = Settings.get(StoredSettings.CARDS_TABLE_COLUMNS_WIDTH_SPACED).split(' ')
        if len(cached_header_geometry) != len(CardsTableHeader):
            cached_header_geometry = [0, 200, 200, 200, 0]
            assert len(cached_header_geometry) == len(CardsTableHeader)

        # Always recalculate first column width.
        cached_header_geometry[CardsTableHeader.Type.value] = ComboBoxCardTypeDelegate.min_editor_width(
            input_model=self.model()) + 20
        self.set_header_sizes(cached_header_geometry)
