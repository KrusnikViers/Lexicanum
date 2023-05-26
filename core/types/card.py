from core.types.card_type import CardType

from core.util import Status


class Card:
    def __init__(self, card_type: CardType,
                 question: str, question_grammar_forms: str, answer: str, note: str,
                 card_id: int | None = None):
        self.card_type: CardType = card_type
        self.question: str = question
        self.question_grammar_forms: str = question_grammar_forms
        self.answer: str = answer
        self.note: str = note
        self.card_id: int | None = card_id

    def validity_status(self) -> Status:
        if not self.question.strip():
            return Status("Question field can not be empty")
        elif not self.answer.strip():
            return Status("Answer field can not be empty")
        elif self.card_type == CardType.Invalid:
            return Status("Choose card type")
        return Status()

    def __str__(self):
        return 'CARD #{} |{} => {}/{}| ({}, {})'.format(
            self.card_id, self.answer, self.question, self.question_grammar_forms, self.card_type.name, self.note)

    @classmethod
    def from_dict(cls, card_dict: dict) -> 'Card':
        return cls(CardType(card_dict['card_type']),
                   card_dict['question'],
                   card_dict['question_grammar_forms'],
                   card_dict['answer'],
                   card_dict['note'],
                   card_dict['card_id'])

    def to_dict(self) -> dict:
        assert self.card_id is not None, "Missing deck normalization?"
        assert self.card_type is not CardType.Invalid
        return {'card_type': self.card_type.value,
                'question': self.question,
                'question_grammar_forms': self.question_grammar_forms,
                'answer': self.answer,
                'note': self.note,
                'card_id': self.card_id,
                }
