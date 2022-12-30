import json

from core.types import Deck
from core.util import Status, StatusOr, UniversalPath


def write_file(deck: Deck, output_path: UniversalPath) -> Status:
    deck.normalize_for_output()
    result = deck.to_dict()
    output_path_str = output_path.as_str()
    try:
        with open(output_path_str, 'w') as output_file:
            json.dump(result, output_file, indent=2, sort_keys=True)
    except PermissionError as e:
        return Status(status='Writing to {} failed: {}'.format(output_path_str, str(e)))
    return Status()


def read_file(input_path: UniversalPath) -> StatusOr[Deck]:
    input_path_str = input_path.as_str()
    try:
        with open(input_path_str) as input_file:
            input_json = json.load(input_file)
            return StatusOr(value=Deck.from_dict(input_json, input_path))
    except (FileNotFoundError, PermissionError) as e:
        return StatusOr(status='Reading from {} failed: {}'.format(input_path_str, str(e)))
