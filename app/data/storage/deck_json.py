import json
from pathlib import Path
from typing import Optional

from app.data.card import Card
from app.data.deck import Deck
from ui.alert import Alert


class DeckJsonWriter:
    @staticmethod
    def write_to_file(deck: Deck, output: Path):
        result = {
            'deck_id': deck.deck_id,
            'deck_name': deck.deck_name,
            'next_card_id': deck.next_card_id,
            'cards': [card.to_dict() for card in deck.cards]
        }
        with open(output, 'w') as output_file:
            json.dump(result, output_file, indent=2, sort_keys=True)

    @staticmethod
    def read_from_file(input_path: Path) -> Optional[Deck]:
        try:
            with open(input_path) as input_file:
                input_json = json.load(input_file)
        except FileNotFoundError:
            Alert.warning('Reading deck from file failed', 'Failed to read file {}'.format(str(input_path)))
            return None

        return Deck(
            deck_id=input_json['deck_id'],
            deck_name=input_json['deck_name'],
            next_card_id=input_json['next_card_id'],
            cards=[Card.from_dict(card_object) for card_object in input_json['cards']]
        )
