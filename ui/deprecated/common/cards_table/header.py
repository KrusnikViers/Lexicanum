from enum import Enum


class CardsTableHeader(Enum):
    Type = 0
    Question = 1
    Answer = 2
    Note = 3

    @classmethod
    def of(cls, index: int) -> 'CardsTableHeader':
        match index:
            case 0:
                return cls.Type
            case 1:
                return cls.Question
            case 2:
                return cls.Answer
            case 3:
                return cls.Note
        assert False
