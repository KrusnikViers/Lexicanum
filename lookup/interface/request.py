from enum import Enum

from core.types import Language


class _SourceType(Enum):
    UNKNOWN = 0
    ANSWER = 1
    QUESTION = 2


class LookupRequest:
    def __init__(self, text: str, language: Language, source_type: _SourceType):
        self.text = text
        self.language = language
        assert source_type != _SourceType.UNKNOWN
        self.source_type = source_type

    @classmethod
    def from_answer(cls, text: str):
        return cls(text, language=Language.EN, source_type=_SourceType.ANSWER)

    @classmethod
    def from_question(cls, text: str):
        return cls(text, language=Language.DE, source_type=_SourceType.QUESTION)
