from PySide2.QtCore import Slot, Signal, Qt
from PySide2.QtWidgets import QWidget

from app.data.card import CardType, Card
from ui.gen.card_input_uic import Ui_CardInput


class CardInput(QWidget):
    accepted = Signal()

    def __init__(self, parent, card_type: CardType, question: str, answer: str,
                 note: str = '', is_default: bool = False):
        super(CardInput, self).__init__(parent)
        self.ui = Ui_CardInput()
        self.ui.setupUi(self)
        self.is_default = is_default
        if is_default:
            self.ui.close.setVisible(False)

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
        self.ui.question.returnPressed.connect(self.ui.accept.click)
        self.ui.answer.returnPressed.connect(self.ui.accept.click)

        # Connect custom slots
        self.ui.close.clicked.connect(self.maybe_close)
        self.ui.accept.clicked.connect(self._accept)

    @classmethod
    def create_default(cls, parent: QWidget):
        return cls(parent, CardType.Invalid, question='', answer='', is_default=True)

    def get_as_card(self) -> Card:
        return Card(self.ui.card_type.currentData(Qt.UserRole),
                    self.ui.question.text().strip(), self.ui.answer.text().strip(),
                    self.ui.note.text().strip())

    @Slot()
    def maybe_close(self):
        if self.is_default:
            return
        self.deleteLater()

    @Slot()
    def _accept(self):
        self.accepted.emit()
