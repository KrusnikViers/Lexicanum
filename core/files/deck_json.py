import json

# TODO(viers): json version check
from core.types import Deck
from core.util import Status, StatusOr, UniversalPath

# Update this field each time the card/deck fields are significantly changed and files from previous version are
# no longer compatible.
_DECK_VERSION = 1
_DECK_VERSION_KEY = 'deck_version'


def write_file(deck: Deck, output_path: UniversalPath) -> Status:
    deck.normalize_for_output()
    result = deck.to_dict()
    result[_DECK_VERSION_KEY] = _DECK_VERSION
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
            file_version = input_json.get(_DECK_VERSION_KEY, 0)
            if file_version != _DECK_VERSION:
                return StatusOr(
                    status='Incompatible deck version: {} vs expected {}'.format(file_version, _DECK_VERSION))
            return StatusOr(value=Deck.from_dict(input_json, input_path))
    except (FileNotFoundError, PermissionError) as e:
        return StatusOr(status='Reading from {} failed: {}'.format(input_path, str(e)))
