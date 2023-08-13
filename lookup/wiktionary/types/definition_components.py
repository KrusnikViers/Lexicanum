from enum import Enum
from typing import NamedTuple

from lookup.wiktionary.types.definition import PartOfSpeech


class DCType(Enum):
    Separator = 0
    PartOfSpeech = 1
    ReadableForm = 2
    Translation = 3


class DCTranslation(NamedTuple):
    lang: str
    text: str

    def __str__(self):
        return 'lang-{}: {}'.format(self.lang, self.text)


class DefinitionComponent:
    _ValueTypes = str | PartOfSpeech | DCTranslation | None

    def __init__(self, level: int, dc_type: DCType, value: _ValueTypes = None):
        self.level = level
        self.dc_type = dc_type
        self.value = value

        match dc_type:
            case DCType.PartOfSpeech:
                assert isinstance(value, PartOfSpeech)
            case DCType.ReadableForm:
                assert isinstance(value, str)
            case DCType.Translation:
                assert isinstance(value, DCTranslation)
            case DCType.Separator:
                assert value is None

    _DCTypeStrValues = {
        DCType.Separator: '---',
        DCType.PartOfSpeech: 'pos',
        DCType.ReadableForm: 'rdf',
        DCType.Translation: 'trl',
    }

    def __str__(self):
        return '|' * self.level + ' -{}: {}'.format(self._DCTypeStrValues[self.dc_type], str(self.value))
