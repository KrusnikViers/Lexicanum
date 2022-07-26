import json
from typing import List


class Card:
    def __init__(self, text_to_learn: str, answer: str):
        self.text_to_learn = text_to_learn
        self.answer = answer


class YandexDictionaryParser:
    @staticmethod
    def _get_gendered_article(gender: str):
        if gender == 'f':
            return 'Die'
        elif gender == 'm':
            return 'Der'
        elif gender == 'n':
            return 'Das'
        return '!{}!'.format(gender)

    @classmethod
    def _parse_noun(cls, definition: dict) -> List[Card]:
        plural_form_description = definition['fl'].split(';')[-1].strip()
        plural_form = plural_form_description
        if plural_form_description == '=':
            plural_form = definition['text']
        elif plural_form_description.startswith('-'):
            plural_form = definition['text'] + plural_form_description[1:]

        text_to_learn = '{} {}, die {}'.format(cls._get_gendered_article(definition['gen']), definition['text'],
                                               plural_form)

        return [Card(text_to_learn, translation['text']) for translation in definition['tr']]

    @classmethod
    def possible_cards_from_yadict_response(cls, response: str) -> List[Card]:
        response_json = json.loads(response)
        if 'def' not in response_json:
            return []
        result = []
        for definition in response_json['def']:
            if definition['pos'] == 'noun':
                result += cls._parse_noun(definition)
            else:
                result.append(Card(definition, 'Can not parse'))
        return result
