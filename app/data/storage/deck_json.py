import json

from app.data.card import Card
from app.data.deck import Deck
from app.data.status_or import Status, StatusOr
from app.data.storage.path import Path


class DeckJsonIO:
    @staticmethod
    def write_to_file(deck: Deck, generic_path: Path) -> Status:
        result = {
            'deck_id': deck.deck_id,
            'deck_name': deck.deck_name,
            'next_card_id': deck.next_card_id,
            'cards': [card.to_dict() for card in deck.cards]
        }
        output_path = generic_path.with_suffix('.json')
        try:
            with open(output_path, 'w') as output_file:
                json.dump(result, output_file, indent=2, sort_keys=True)
        except PermissionError as e:
            return Status.from_status('Writing to {} failed: {}'.format(output_path, str(e)))
        return Status.no_error()

    @staticmethod
    def read_from_file(input_path: Path) -> StatusOr[Deck]:
        str_input_path = input_path.as_str()
        try:
            with open(str_input_path) as input_file:
                input_json = json.load(input_file)
        except (FileNotFoundError, PermissionError) as e:
            return StatusOr.from_status('Reading from {} failed: {}'.format(str_input_path, str(e)))

        return StatusOr.from_value(Deck(
            deck_id=input_json['deck_id'],
            deck_name=input_json['deck_name'],
            next_card_id=input_json['next_card_id'],
            cards=[Card.from_dict(card_object) for card_object in input_json['cards']],
            file_path=input_path
        ))
