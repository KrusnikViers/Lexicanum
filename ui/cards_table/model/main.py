from copy import deepcopy
from typing import List

from PySide6.QtCore import QModelIndex

from app.data import Card, CardType, Deck, Status
from ui.cards_table.model.base import BaseCardsModel


class MainCardsModel(BaseCardsModel):
    def __init__(self, displayed_deck: Deck):
        super(MainCardsModel, self).__init__()
        self.deck: Deck = displayed_deck
        self.displayed_rows: List[Card] = []
        self.reset_deck(displayed_deck)

    @staticmethod
    def _passes_input_filter(card: Card, input_filter: Card):
        return (input_filter.card_type == CardType.Invalid or input_filter.card_type == card.card_type) and \
               (input_filter.question == '' or input_filter.question.lower() in card.question.lower()) and \
               (input_filter.answer == '' or input_filter.answer.lower() in card.answer.lower())

    def refresh_displayed_rows(self, input_filter: Card | None = None):
        self.beginResetModel()
        self.displayed_rows = [card for card in self.deck.cards if
                               input_filter is None or self._passes_input_filter(card, input_filter)]
        self.endResetModel()

    def get_card(self, row: int) -> Card:
        return self.displayed_rows[row]

    def add_card(self, card: Card) -> Status:
        if card.card_type == CardType.Invalid:
            return Status.from_status('Card type can not be empty')
        self.beginInsertRows(QModelIndex(), 0, 0)
        self.deck.cards.insert(0, deepcopy(card))
        self.displayed_rows.insert(0, self.deck.cards[0])
        self.endInsertRows()
        return Status.no_error()

    def remove_card(self, index: QModelIndex):
        row = index.row()
        self.beginRemoveRows(QModelIndex(), row, row)
        assert 0 <= row <= len(self.displayed_rows)
        self.deck.cards.remove(self.displayed_rows[row])
        del self.displayed_rows[row]
        self.endRemoveRows()

    def cards_count(self) -> int:
        return len(self.displayed_rows)

    def reset_deck(self, new_deck: Deck):
        self.deck = new_deck
        self.refresh_displayed_rows()
