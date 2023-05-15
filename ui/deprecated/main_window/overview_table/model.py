from copy import deepcopy
from typing import List, Any

from PySide6.QtCore import QModelIndex, Signal, Qt
from PySide6.QtGui import QColor

from core.types import Deck, Card, CardType
from ui.common.cards_table import CardsTableModel


class OverviewCardsTableModel(CardsTableModel):
    deck_updated = Signal()

    def __init__(self, displayed_deck: Deck):
        super().__init__()
        self.deck: Deck = displayed_deck
        self.displayed_rows: List[Card] = []
        self.reset_deck(displayed_deck)

    def highlight_color(self, index: QModelIndex) -> QColor | None:
        return None

    def supports_invalid_card_type(self) -> bool:
        return False

    @staticmethod
    def _passes_display_filter(card: Card, type_filter, question_filter, answer_filter):
        return (type_filter == CardType.Invalid or type_filter == card.card_type) and \
               (not question_filter or question_filter in card.question.lower()) and \
               (not answer_filter or answer_filter in card.answer.lower())

    def refresh_displayed_rows(self, card_in_input: Card | None = None):
        self.beginResetModel()
        if card_in_input is None:
            self.displayed_rows = self.deck.cards
        else:
            type_filter = card_in_input.card_type
            question_filter = card_in_input.question.strip().lower()
            answer_filter = card_in_input.answer.strip().lower()
            self.displayed_rows = [card for card in self.deck.cards if
                                   self._passes_display_filter(card, type_filter, question_filter, answer_filter)]
        self.endResetModel()

    def _on_deck_updated(self):
        if not self.deck.was_updated:
            self.deck.was_updated = True
            self.deck_updated.emit()

    def setData(self, index: QModelIndex, value: Any, role: int = None) -> bool:
        result = super().setData(index, value, role)
        if role == Qt.DisplayRole:
            self._on_deck_updated()
        return result

    def get_card(self, row: int) -> Card:
        return self.displayed_rows[row]

    def add_card(self, card: Card):
        assert card.is_valid()
        self.beginInsertRows(QModelIndex(), 0, 0)
        self.deck.cards.insert(0, deepcopy(card))
        self.displayed_rows.insert(0, self.deck.cards[0])
        self.endInsertRows()
        self._on_deck_updated()

    def remove_card(self, index: QModelIndex):
        row = index.row()
        self.beginRemoveRows(QModelIndex(), row, row)
        assert 0 <= row <= len(self.displayed_rows)
        self.deck.cards.remove(self.displayed_rows[row])
        del self.displayed_rows[row]
        self.endRemoveRows()
        self._on_deck_updated()

    def cards_count(self) -> int:
        return len(self.displayed_rows)

    def reset_deck(self, new_deck: Deck):
        self.deck = new_deck
        self.refresh_displayed_rows()
