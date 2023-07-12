from PySide6.QtCore import QTimer, Slot
from PySide6.QtWidgets import QStatusBar, QWidget, QLabel


class StatusBar(QStatusBar):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.setSizeGripEnabled(False)
        self.setStyleSheet('color: #666; background-color: #fff; margin-left: 9px;')

        self.main_message: str = ''
        self.status_label = QLabel()
        self.addWidget(self.status_label, stretch=1)
        # QStatusBar have an issue with styling temporary messages, so implement temporary messages manually.
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.reset_on_timer)

        self.show_message(self.main_message)

    @Slot(str)
    def show_timed_message(self, message: str):
        self.timer.stop()
        self.timer.start()
        self.status_label.setText(message)

    def show_message(self, message: str):
        self.main_message = message
        if not self.timer.isActive():
            self.status_label.setText(self.main_message)

    @Slot()
    def reset_on_timer(self):
        self.status_label.setText(self.main_message)
