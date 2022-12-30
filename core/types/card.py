from core.types.card_type import CardType


class Card:
    def __init__(self, card_type: CardType,
                 question: str, answer: str, note: str,
                 card_id: int | None = None):
        self.card_type: CardType = card_type
        self.question: str = question
        self.answer: str = answer
        self.note: str = note
        self.card_id: int | None = card_id

    def is_valid(self) -> bool:
        if not self.question.strip() or not self.answer.strip():
            return False
        if self.card_type == CardType.Invalid:
            return False
        return True

    @classmethod
    def from_dict(cls, card_dict: dict) -> 'Card':
        return cls(CardType(card_dict['card_type']),
                   card_dict['question'],
                   card_dict['answer'],
                   card_dict['note'],
                   card_dict['card_id'])

    def to_dict(self) -> dict:
        assert self.card_id is not None, "Missing deck normalization?"
        assert self.card_type is not CardType.Invalid
        return {'card_type': self.card_type.value,
                'question': self.question,
                'answer': self.answer,
                'note': self.note,
                'card_id': self.card_id,
                }
