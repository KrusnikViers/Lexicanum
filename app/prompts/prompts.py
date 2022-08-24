import json
from typing import List

from app.data.card import Card
from app.data.language import Language
from app.prompts.nouns import construct_noun_cards


def construct_cards_from_dictionary_response(language: Language, raw_dictionary_response: str) -> List[Card]:
    response_json = json.loads(raw_dictionary_response)
    if 'def' not in response_json:
        return []

    result: List[Card] = []
    for definition in response_json['def']:
        if definition['pos'] == 'noun':
            result += construct_noun_cards(language, definition)
        else:
            print('Could not parse: {}'.format(definition))

    return result
