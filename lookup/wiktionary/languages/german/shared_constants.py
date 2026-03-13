from lookup.wiktionary.types import PartOfSpeech

POS_MAP = {
    'Substantiv': PartOfSpeech.Noun,
    'Toponym': PartOfSpeech.Noun,
    'Adjektiv': PartOfSpeech.Adjective,
    'Verb': PartOfSpeech.Verb,
    'Adverb': PartOfSpeech.Adverb,
    'Lokaladverb': PartOfSpeech.Adverb,

    'Pronomen': PartOfSpeech.Pronoun,
    'Demonstrativpronomen': PartOfSpeech.Pronoun,
    'Präposition': PartOfSpeech.Preposition,
    'Konjunktion': PartOfSpeech.Conjunction,
    'Subjunktion': PartOfSpeech.Conjunction,
    'Interjektion': PartOfSpeech.Interjection,
    'Grußformel': PartOfSpeech.Interjection,
    'Artikel': PartOfSpeech.Article,
    'Gradpartikel': PartOfSpeech.Particle,
    'Negationspartikel': PartOfSpeech.Particle,
    'Numerale': PartOfSpeech.Numeral,

    'Redewendung': PartOfSpeech.Phrase,
    'Wortverbindung': PartOfSpeech.Phrase,
}

POS_KEY = 'Wortart'
