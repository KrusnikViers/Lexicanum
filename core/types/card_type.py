from enum import Enum


class CardType(Enum):
    # Cards with this type could not be exported or saved in project files.
    Invalid = 0

    # Main parts of speech
    Noun = 1
    Adjective = 2
    Verb = 3
    Adverb = 4

    # Other parts of speech
    Particle = 11
    Conjunction = 12
    Pronoun = 13
    Interjection = 14

    # Complex translatable concepts
    Phrase = 100

    # One-way questions
    Rule = 200

    def display_name(self):
        if self == CardType.Invalid:
            return ''
        return self.name
