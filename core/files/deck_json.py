import json

from core.types import Deck
from core.util import Status, StatusOr, UniversalPath


def write_file(deck: Deck, output_path: UniversalPath) -> Status:
    deck.normalize_for_output()
    result = deck.to_dict()
    try:
        with open(str(output_path), 'w') as output_file:
            json.dump(result, output_file, indent=2, sort_keys=True)
    except PermissionError as e:
        return Status(status='Writing to {} failed: {}'.format(output_path, str(e)))
    return Status()


def read_file(input_path: UniversalPath) -> StatusOr[Deck]:
    try:
        with open(str(input_path)) as input_file:
            input_json = json.load(input_file)
            return StatusOr(value=Deck.from_dict(input_json, input_path))
    except (FileNotFoundError, PermissionError) as e:
        return StatusOr(status='Reading from {} failed: {}'.format(input_path, str(e)))
