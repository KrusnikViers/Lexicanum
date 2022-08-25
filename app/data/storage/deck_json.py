import json
from pathlib import Path
from typing import Optional

from app.data.card import Card
from app.data.deck import Deck
from ui.alert import Alert

# Modify when incompatible changes are made to the underlying model
_JSON_VERSION = 1


class DeckJsonWriter:
    @staticmethod
    def write_to_file(deck: Deck, output: Path):
        result = {
            'deck_version': _JSON_VERSION,
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

        if input_json['deck_version'] != _JSON_VERSION:
            Alert.warning('JSON file has incompatible version',
                          '{} file has JSON of v.{}, but the app supports v.{} only'.format(str(input_path),
                                                                                            input_json['deck_version'],
                                                                                            _JSON_VERSION))
            return None

        return Deck(
            deck_id=input_json['deck_id'],
            deck_name=input_json['deck_name'],
            next_card_id=input_json['next_card_id'],
            cards=[Card.from_dict(card_object) for card_object in input_json['cards']]
        )
