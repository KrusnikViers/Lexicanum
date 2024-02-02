from enum import Enum


class CardsTableHeader(Enum):
    Type = 0
    Question = 1
    Grammar = 2
    IPA = 3
    QExample = 4
    Answer = 5
    AExample = 6
    Note = 7

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
                return cls.IPA
            case 4:
                return cls.QExample
            case 5:
                return cls.Answer
            case 6:
                return cls.AExample
            case 7:
                return cls.Note
        assert False

    def display_name(self) -> str:
        if self == self.IPA:
            return 'Pronunciation (IPA)'
        elif self == self.QExample:
            return 'Example (Question)'
        elif self == self.AExample:
            return 'Example (Answer)'
        else:
            return self.name
