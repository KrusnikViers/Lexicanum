from PySide6.QtWidgets import QWidget, QHeaderView

from ui.cards_table.delegate import CardTypeDelegate, LineEditSimpleDelegate
from ui.cards_table.model.abstract import CardsModelHeader, AbstractCardsModel
from ui.cards_table.view.abstract import AbstractCardsTableView


class ListingCardsTableView(AbstractCardsTableView):
    def __init__(self, parent: QWidget, model: AbstractCardsModel):
        super(ListingCardsTableView, self).__init__(parent, model)

        self.setItemDelegateForColumn(CardsModelHeader.Type.value, CardTypeDelegate.instance)
        self.setItemDelegateForColumn(CardsModelHeader.Note.value, LineEditSimpleDelegate.instance)
        self.setItemDelegateForColumn(CardsModelHeader.Question.value, LineEditSimpleDelegate.instance)
        self.setItemDelegateForColumn(CardsModelHeader.Answer.value, LineEditSimpleDelegate.instance)

        self.horizontalHeader().setVisible(False)
        self.horizontalHeader().setSectionResizeMode(CardsModelHeader.Type.value, QHeaderView.ResizeMode.Fixed)
        self.horizontalHeader().setSectionResizeMode(CardsModelHeader.Question.value, QHeaderView.ResizeMode.Fixed)
        self.horizontalHeader().setSectionResizeMode(CardsModelHeader.Answer.value, QHeaderView.ResizeMode.Fixed)
        self.horizontalHeader().setSectionResizeMode(CardsModelHeader.Note.value, QHeaderView.ResizeMode.Stretch)
