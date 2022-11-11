from pprint import pformat
from typing import List

from app.data import Card, CardType, Language
from app.translation_lookup.prompts import german


class PromptConstructor:
    # Key: API key for word type
    # Value: Internal enum value for type
    _CARD_TYPE_LOOKUP = {
        'noun': CardType.Noun,
        'adjective': CardType.Adjective,
        'verb': CardType.Verb,
        'adverb': CardType.Adverb,
        'particle': CardType.Particle,
        'conjunction': CardType.Conjunction,
        'pronoun': CardType.Pronoun,
        'interjection': CardType.Interjection
    }

    _SPECIAL_HANDLERS = {
        (Language.DE, CardType.Noun): german.construct_noun_prompts,
    }

    @staticmethod
    def construct(language: Language, definition: dict) -> List[Card]:
        if definition['pos'] not in PromptConstructor._CARD_TYPE_LOOKUP:
            print('Unhandled type of word:\n{}'.format(pformat(definition, indent=2)))
            return []
        card_type = PromptConstructor._CARD_TYPE_LOOKUP[definition['pos']]

        if (language, card_type) in PromptConstructor._SPECIAL_HANDLERS:
            constructor_fn = PromptConstructor._SPECIAL_HANDLERS[(language, card_type)]
            return constructor_fn(definition)

        # Trivial prompt construction
        return [Card(card_type,
                     question=definition['text'].capitalize(),
                     answer=translation['text'].capitalize(),
                     note='')
                for translation in definition['tr']]
