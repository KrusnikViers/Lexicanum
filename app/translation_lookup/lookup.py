import json
from collections import namedtuple
from typing import List

from app.data.card import Card
from app.translation_lookup.dictionary.api import get_raw_translations_list
from app.translation_lookup.prompts.nouns import construct_noun_cards

LookupData = namedtuple('LookupData', 'word language')


class Lookup:
    @staticmethod
    def suggestions(lookup_data: LookupData) -> List[Card]:
        raw_translations = get_raw_translations_list(lookup_data.word, lookup_data.language)
        response_json = json.loads(raw_translations)
        if 'def' not in response_json:
            return []

        result: List[Card] = []
        for definition in response_json['def']:
            if definition['pos'] == 'noun':
                result += construct_noun_cards(lookup_data.language, definition)
            else:
                print('Could not parse: {}'.format(definition))

        return result
