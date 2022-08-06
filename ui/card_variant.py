from PySide2.QtCore import Slot, Signal
from PySide2.QtWidgets import QWidget

from core.card import CardType
from ui.gen.card_variant_uic import Ui_CardVariant


class CardVariant(QWidget):
    accepted = Signal()

    def __init__(self, parent, card_type: CardType = CardType.Phrase,  #
                 question: str = '', answer: str = '', note: str = ''):
        super(CardVariant, self).__init__(parent)

        self.ui = Ui_CardVariant()
        self.ui.setupUi(self)
        for added_card_type in CardType:
            if added_card_type is CardType.Invalid:
                continue
            self.ui.card_type.addItem(added_card_type.name, added_card_type)
            if added_card_type == card_type:
                self.ui.card_type.setCurrentIndex(self.ui.card_type.count() - 1)
        self.ui.question.setText(question)
        self.ui.answer.setText(answer)
        self.ui.note.setText(note)

        self.ui.drop.clicked.connect(self._drop)
        self.ui.add.clicked.connect(self._accept)

    def disable_drop(self):
        self.ui.drop.setEnabled(False)

    @Slot()
    def _drop(self):
        self.deleteLater()

    @Slot()
    def _accept(self):
        self.accepted.emit()
        self._drop()
