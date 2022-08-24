from typing import Optional


class DeckMeta:
    _deck_id = Optional[int]
    _next_card_id = 0

    @classmethod
    def get_card_id(cls):
        new_id = cls._next_card_id
        cls._next_card_id += 1
        return new_id

    @classmethod
    def reset_deck_id(cls):
        cls._deck_id = None

    @classmethod
    def from_dict(cls, deck_dict: dict):
        _deck_id = deck_dict['deck_id']
        _next_card_id = deck_dict['next_card_id']

    @classmethod
    def to_dict(cls) -> dict:
        return {
            'deck_id': cls._deck_id,
            'next_card_id': cls._next_card_id
        }
