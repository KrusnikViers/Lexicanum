import json
from typing import List

from core.card import Card, CardType, Language


def _get_gendered_article(gender: str):
    if gender == 'f':
        return 'Die'
    elif gender == 'm':
        return 'Der'
    elif gender == 'n':
        return 'Das'
    return '!{}!'.format(gender)


def _parse_noun(definition: dict) -> List[Card]:
    plural_form_description = definition['fl'].split(';')[-1].strip()
    plural_form = plural_form_description
    if plural_form_description == '=':
        plural_form = definition['text']
    elif plural_form_description.startswith('-'):
        plural_form = definition['text'] + plural_form_description[1:]

    text_to_learn = '{} {}, die {}'.format(_get_gendered_article(definition['gen']), definition['text'],
                                           plural_form)

    return [Card(CardType.Noun, text_to_learn, translation['text']) for translation in definition['tr']]


def get_possible_cards_for(source_language: Language, api_response: str) -> List[Card]:
    response_json = json.loads(api_response)
    if 'def' not in response_json:
        return []
    result = []
    for definition in response_json['def']:
        if definition['pos'] == 'noun':
            result += _parse_noun(definition)
        else:
            print('Could not parse: {}'.format(definition))
    return result
