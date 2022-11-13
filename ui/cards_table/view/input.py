from PySide6.QtWidgets import QWidget, QHeaderView, QSizePolicy

from app.data import Settings, StoredSettings
from ui.cards_table.delegate import CardTypeDelegate, LineEditSimpleDelegate, LineEditLookupDelegate
from ui.cards_table.model.abstract import CardsModelHeader, AbstractCardsModel
from ui.cards_table.view.abstract import AbstractCardsTableView
from ui.shared.shortcuts import ShortcutCommand


class InputCardsTableView(AbstractCardsTableView):
    def __init__(self, parent: QWidget, model: AbstractCardsModel):
        super(InputCardsTableView, self).__init__(parent, model)

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

    def store_geometry(self):
        sizes_serialized = ' '.join(map(str, self.header_sizes()))
        Settings.set(StoredSettings.SUMMARY_TABLE_COLUMNS_WIDTH_SPACED, sizes_serialized)

    def restore_geometry(self):
        sizes_packed = Settings.get(StoredSettings.SUMMARY_TABLE_COLUMNS_WIDTH_SPACED)
        sizes = [] if len(sizes_packed) == 0 else [int(size) for size in sizes_packed.split(' ')]
        if len(sizes) != len(CardsModelHeader):
            print('Table geometry invalid: {}, restoring default'.format(sizes))
            sizes = [120, 250, 250, 0]
            assert len(sizes) == len(CardsModelHeader)
        self.set_header_sizes(sizes)
