from typing import List

from app.data import CardType, Card


def _gendered_article(gender: str):
    if gender == 'f':
        return 'Die'
    elif gender == 'm':
        return 'Der'
    elif gender == 'n':
        return 'Das'
    return '!Wrong gender: {}!'.format(gender)


def _plural_form(word: str, forms_list: str):
    plural_form_encoded = forms_list.split(';')[-1].strip()
    if plural_form_encoded == '=':
        return word
    if plural_form_encoded.startswith('-'):
        return word + plural_form_encoded[1:]
    return plural_form_encoded


# For a single word, returns all possible translated prompts.
def construct_noun_prompts(definition: dict) -> List[Card]:
    print(definition)
    word_to_learn = '{} {}, die {}'.format(_gendered_article(definition['gen']),
                                           definition['text'],
                                           _plural_form(definition['text'], definition['fl']))
    return [Card(CardType.Noun, question=word_to_learn, answer=translation['text'].capitalize(), note='')
            for translation in definition['tr']]
