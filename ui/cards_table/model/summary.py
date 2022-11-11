from copy import deepcopy

from PySide6.QtCore import QModelIndex

from app.data import Card, CardType, Deck
from ui.cards_table.model.abstract import AbstractCardsModel
from ui.shared.shortcuts import ShortcutCommand


class SummaryCardsModel(AbstractCardsModel):
    def __init__(self, displayed_deck: Deck):
        super(SummaryCardsModel, self).__init__()
        self.deck = displayed_deck
        self.stub_card = Card(CardType.Phrase, '', '', '')

    def card_by_row(self, row: int) -> Card:
        if row > 0:
            return self.deck.cards[row - 1]
        return self.stub_card

    def execute_shortcut_action(self, row: int, command: ShortcutCommand):
        if row == 0 and command in (ShortcutCommand.ENTER, ShortcutCommand.ENTER_AND_CONTINUE):
            self.new_row_from_stub()
        if row == 0 and command in (ShortcutCommand.ENTER, ShortcutCommand.CLEAR):
            self.clean_stub_data()
        if row != 0 and command == ShortcutCommand.CLEAR:
            self.remove_row(row)

    def remove_row(self, row: int) -> None:
        assert 0 < row <= len(self.deck.cards)
        self.beginRemoveRows(QModelIndex(), row, row)
        del self.deck.cards[row - 1]
        self.endRemoveRows()

    def clean_stub_data(self) -> None:
        self.stub_card.answer = ''
        self.stub_card.question = ''
        self.stub_card.note = ''
        self.refresh_visible_contents(0)

    def new_row(self, card: Card):
        _ROW_INDEX = 1
        self.beginInsertRows(QModelIndex(), _ROW_INDEX, _ROW_INDEX)
        self.deck.cards.insert(0, deepcopy(card))
        self.endInsertRows()
        self.refresh_visible_contents(_ROW_INDEX)

    def new_row_from_stub(self):
        self.new_row(self.stub_card)

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        # First row is a stub, to add new records.
        return len(self.deck.cards) + 1
