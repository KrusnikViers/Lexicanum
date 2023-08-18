from enum import Enum


class CardsTableHeader(Enum):
    Type = 0
    Question = 1
    Grammar = 2
    Answer = 3
    IPA = 4
    Note = 5

    @classmethod
    def of(cls, index: int) -> 'CardsTableHeader':
        match index:
            case 0:
                return cls.Type
            case 1:
                return cls.Question
            case 2:
                return cls.Grammar
            case 3:
                return cls.Answer
            case 4:
                return cls.IPA
            case 5:
                return cls.Note
        assert False
