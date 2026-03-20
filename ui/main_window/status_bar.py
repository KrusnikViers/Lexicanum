import enum

from PySide6.QtCore import QTimer, Slot
from PySide6.QtWidgets import QStatusBar, QWidget, QLabel


class StatusType(enum.Enum):
    Info = 'info'
    Error = 'error'


class StatusBar(QStatusBar):
    def __init__(self, parent: QWidget, main_message: str = ''):
        super().__init__(parent)
        self.setSizeGripEnabled(False)

        self._persistent_status: str = main_message
        self._ui_status_label = QLabel()
        self.addWidget(self._ui_status_label, stretch=1)

        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.setInterval(5000)
        self._timer.timeout.connect(self._reset_on_timer)

        self.set_status(self._persistent_status)

    def _display_status_message(self, message: str, status_type: StatusType) -> None:
        # QStatusBar does not style temporary messages properly, thus the manual implementation.
        match status_type:
            case StatusType.Info:
                self._ui_status_label.setStyleSheet('color: #666; background-color: #fff; padding-left: 5px;')
            case StatusType.Error:
                self._ui_status_label.setStyleSheet('color: #900; background-color: #fff; padding-left: 5px;')
        self._ui_status_label.setText(message)

    @Slot(str)
    def set_temporary_status(self, message: str, status_type: StatusType = StatusType.Info) -> None:
        self._timer.stop()
        self._timer.start()
        self._display_status_message(message, status_type)

    @Slot(str)
    def set_status(self, message: str) -> None:
        self._persistent_status = message
        if not self._timer.isActive():
            self._display_status_message(self._persistent_status, StatusType.Info)

    @Slot()
    def _reset_on_timer(self) -> None:
        self._display_status_message(self._persistent_status, StatusType.Info)
