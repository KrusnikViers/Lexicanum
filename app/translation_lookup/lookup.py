import itertools
import json
from collections import namedtuple
from typing import List

from app.data.card import Card
from app.translation_lookup.api import get_raw_translations_list
from app.translation_lookup.prompts.constructor import PromptConstructor

LookupData = namedtuple('LookupData', 'word language')


class Lookup:
    @staticmethod
    def suggestions(lookup_data: LookupData) -> List[Card]:
        raw_translations = get_raw_translations_list(lookup_data.word, lookup_data.language)
        response_json = json.loads(raw_translations)
        if 'def' not in response_json:
            return []
        results_per_definition = [PromptConstructor.construct(lookup_data.language, definition)
                                  for definition in response_json['def']]
        return list(itertools.chain(*results_per_definition))
