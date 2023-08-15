from lookup.wiktionary.types import PartOfSpeech

POS_MAP = {
    'Substantiv': PartOfSpeech.Noun,
    'Toponym': PartOfSpeech.Noun,
    'Adjektiv': PartOfSpeech.Adjective,
    'Verb': PartOfSpeech.Verb,
    'Adverb': PartOfSpeech.Adverb,

    'Pronomen': PartOfSpeech.Pronoun,
    'Demonstrativpronomen': PartOfSpeech.Pronoun,
    'Präposition': PartOfSpeech.Preposition,
    'Konjunktion': PartOfSpeech.Conjunction,
    'Interjektion': PartOfSpeech.Interjection,
    'Grußformel': PartOfSpeech.Interjection,
    'Artikel': PartOfSpeech.Article,
    'Gradpartikel': PartOfSpeech.Particle,
    'Numerale': PartOfSpeech.Numeral,

    'Redewendung': PartOfSpeech.Phrase,
    'Wortverbindung': PartOfSpeech.Phrase,
}

# Noun = 1  # Incl. Proper Nouns
#     Adjective = 2
#     Verb = 3
#     Adverb = 4
#
#     # Other parts of speech
#     Pronoun = 11
#     Preposition = 12  # Incl. Postposition
#     Conjunction = 13
#     Interjection = 14
#     Article = 15
#     Particle = 16
#     Numeral = 17
#
#     # Complex translatable concepts
#     Phrase = 100

POS_KEY = 'Wortart'

SUPPORTED_LANGUAGES = ('Deutsch',)
