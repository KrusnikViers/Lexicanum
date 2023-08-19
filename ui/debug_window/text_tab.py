from PySide6.QtWidgets import QWidget

from ui.gen.debug_window.text_tab_uic import Ui_TextDebug


class TextTab(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.ui = Ui_TextDebug()
        self.ui.setupUi(self)
