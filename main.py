import sys
from typing import Self, ClassVar

from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QApplication

from ui.main_window import main_window


class Application(QApplication):
    _app_instance: ClassVar[Self | None] = None

    def __init__(self):
        super().__init__(sys.argv)

        self.main_window = main_window.MainWindow()
        self.main_window.application_exit_requested.connect(self.on_exit_requested)

    @classmethod
    def get_or_create(cls) -> Self:
        if cls._app_instance is None:
            QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
            cls._app_instance = cls()
        return cls._app_instance

    @Slot()
    def on_exit_requested(self):
        # Do any pre-exit checks here.
        # Return before the following lines to interrupt application closing.
        self.main_window.close()
        self.quit()


if __name__ == "__main__":  # pragma: no cover
    sys.exit(Application.get_or_create().exec())
