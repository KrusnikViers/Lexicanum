from lookup.wiktionary.types import PartOfSpeech

POS_MAP = {
    'noun': PartOfSpeech.Noun,
    'proper noun': PartOfSpeech.Noun,
    'plural noun': PartOfSpeech.Noun,
    'verb': PartOfSpeech.Verb,
    'adj': PartOfSpeech.Adjective,
    'adjective': PartOfSpeech.Adjective,
    'adv': PartOfSpeech.Adverb,
    'adverb': PartOfSpeech.Adverb,

    'det': PartOfSpeech.Pronoun,
    'pron': PartOfSpeech.Pronoun,
    'prep': PartOfSpeech.Preposition,
    'con': PartOfSpeech.Conjunction,
    'conjunction': PartOfSpeech.Conjunction,
    'interj': PartOfSpeech.Interjection,
    'article': PartOfSpeech.Article,
    'part': PartOfSpeech.Particle,
    'numeral': PartOfSpeech.Numeral,

    'phrase': PartOfSpeech.Phrase,
}

POS_KEY_PREFIX = 'en-'
POS_KEY_FULL = 'head'
