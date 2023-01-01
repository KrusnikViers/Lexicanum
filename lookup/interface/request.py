from enum import Enum

from core.types import Language


class LookupRequest:
    class Type(Enum):
        UNKNOWN = 0
        ANSWER = 1
        QUESTION = 2

    def __init__(self, text: str, source_language: Language, target_language: Language, source_type: Type):
        self.text = text
        self.source_language = source_language
        self.target_language = target_language
        assert source_type != LookupRequest.Type.UNKNOWN
        self.source_type = source_type

    @classmethod
    def from_answer(cls, text: str):
        return cls(text,
                   source_language=Language.EN, target_language=Language.DE,
                   source_type=LookupRequest.Type.ANSWER)

    @classmethod
    def from_question(cls, text: str):
        return cls(text,
                   source_language=Language.DE, target_language=Language.EN,
                   source_type=LookupRequest.Type.QUESTION)
