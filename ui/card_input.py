from PySide2.QtCore import Slot, Signal, Qt
from PySide2.QtWidgets import QWidget

from app.data.card import CardType, Card
from ui.gen.card_input_uic import Ui_CardInput


class CardInput(QWidget):
    accepted = Signal()

    def __init__(self, parent, card_type: CardType, question: str, answer: str,
                 note: str = '', is_prompt: bool = True):
        super(CardInput, self).__init__(parent)
        self.ui = Ui_CardInput()
        self.ui.setupUi(self)
        self.is_prompt = is_prompt
        if not is_prompt:
            self.ui.drop.setVisible(False)

        for added_card_type in CardType:
            if added_card_type is CardType.Invalid:
                continue
            self.ui.card_type.addItem(added_card_type.name, added_card_type)
            if added_card_type == card_type:
                self.ui.card_type.setCurrentIndex(self.ui.card_type.count() - 1)
        self.ui.question.setText(question)
        self.ui.answer.setText(answer)
        self.ui.note.setText(note)

        # Connect build-ins
        self.ui.question.returnPressed.connect(self.ui.add.click)
        self.ui.answer.returnPressed.connect(self.ui.add.click)

        # Connect custom slots
        self.ui.drop.clicked.connect(self.maybe_drop)
        self.ui.add.clicked.connect(self._accept)

    def get_as_card(self) -> Card:
        return Card(self.ui.card_type.currentData(Qt.UserRole),
                    self.ui.question.text().strip(), self.ui.answer.text().strip(),
                    self.ui.note.text().strip())

    @Slot()
    def maybe_drop(self):
        if not self.is_prompt:
            return
        self.deleteLater()

    @Slot()
    def _accept(self):
        # TODO: Add validation
        self.accepted.emit()


def construct_input_from_card(parent: QWidget, card: Card) -> CardInput:
    return CardInput(parent, card.card_type, card.question, card.answer, card.note, is_prompt=True)


def construct_default_input(parent: QWidget) -> CardInput:
    return CardInput(parent, CardType.Phrase, question='', answer='', note='', is_prompt=False)
