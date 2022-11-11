import json

from app.data.base.deck import Deck
from app.data.base.status_or import Status, StatusOr
from app.data.filesystem.path import Path


class DeckJsonIO:
    @staticmethod
    def write_to_file(deck: Deck, generic_path: Path) -> Status:
        deck.normalize_for_output()
        result = deck.to_dict()
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
                return StatusOr.from_value(Deck.from_dict(input_json, input_path))
        except (FileNotFoundError, PermissionError) as e:
            return StatusOr.from_status('Reading from {} failed: {}'.format(str_input_path, str(e)))
