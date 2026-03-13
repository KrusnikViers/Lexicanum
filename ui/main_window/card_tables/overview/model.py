from copy import deepcopy
from typing import Any, List

from PySide6.QtCore import QModelIndex, Signal, Slot

from core.types import Deck, Card
from ui.main_window.card_tables.base.model import CardsTableModel


class OverviewCardsTableModel(CardsTableModel):
    deck_updated = Signal()

    def __init__(self, displayed_deck: Deck):
        super().__init__()
        self.deck: Deck = displayed_deck
        # Separate list with the same cards
        self.visible_cards: List[Card] = []
        self.reset_deck(displayed_deck)

    @Slot(str)
    def filter_by_answer(self, filter_text: str):
        self.beginResetModel()
        self.visible_cards = [x for x in self.deck.cards if filter_text.lower() in x.answer.lower()]
        self.endResetModel()

    @Slot(str)
    def filter_by_question(self, filter_text: str):
        self.beginResetModel()
        self.visible_cards = [x for x in self.deck.cards if filter_text.lower() in x.question.lower()]
        self.endResetModel()

    # Virtual methods
    def supports_invalid_card_type(self) -> bool:
        return False

    def get_card(self, row: int) -> Card:
        return self.visible_cards[row]

    def insert_card(self, card: Card):
        assert card.validity_status()
        self.beginInsertRows(QModelIndex(), 0, 0)
        self.visible_cards.insert(0, deepcopy(card))
        self.deck.cards.insert(0, self.visible_cards[0])
        self.endInsertRows()

    def remove_card(self, index: QModelIndex):
        row = index.row()
        self.beginRemoveRows(QModelIndex(), row, row)
        assert 0 <= row <= len(self.visible_cards)
        self.deck.cards.remove(self.visible_cards[row])
        del self.visible_cards[row]
        self.endRemoveRows()

    def cards_count(self) -> int:
        return len(self.visible_cards)

    # Own methods
    def setData(self, index: QModelIndex, value: Any, role: int = None) -> bool:
        result = super().setData(index, value, role)
        return result

    def reset_deck(self, new_deck: Deck):
        self.beginResetModel()
        self.deck = new_deck
        self.visible_cards = [x for x in self.deck.cards]
        self.endResetModel()
