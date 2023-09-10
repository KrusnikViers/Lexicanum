from PySide6.QtCore import Slot
from PySide6.QtWidgets import QDialog, QWidget, QAbstractButton, QDialogButtonBox

from ui.gen.unsaved_changes_dialog.unsaved_changes_dialog_uic import Ui_UnsavedChangesDialog


class UnsavedChangesDialog(QDialog):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.answer: bool | None = None
        self.ui = Ui_UnsavedChangesDialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.clicked.connect(self.on_answer)
        self.show()

    @Slot(QAbstractButton)
    def on_answer(self, button: QAbstractButton):
        match self.ui.buttonBox.buttonRole(button):
            case QDialogButtonBox.ButtonRole.AcceptRole:
                self.answer = True
                self.accept()
            case QDialogButtonBox.ButtonRole.DestructiveRole:
                self.answer = False
        self.reject()

    @classmethod
    def save_before_action(cls, parent_widget: QWidget) -> bool | None:
        dialog = cls(parent_widget)
        dialog.exec()
        return dialog.answer
