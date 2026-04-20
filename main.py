import logging
import sys

from PySide6.QtCore import Slot, Qt, QObject, Signal, SignalInstance
from PySide6.QtWidgets import QApplication

from anki import wrapper
from base import logs
from ui.main_window import main_window


class Orchestrator(QObject):
    """Class, responsible for setting up and connecting all the primary modules."""

    exit_requested: SignalInstance = Signal()

    def __init__(self):
        super().__init__()

        QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
        # TODO: Restore when settings window is implemented.
        # logs.update_logging_configuration(settings.LOGS_VERBOSITY.get())
        logs.update_logging_configuration('info')

        self.anki_wrapper = wrapper.AnkiWrapper()

        self.main_window = main_window.MainWindow(anki_wrapper=self.anki_wrapper)
        self.main_window.exit_requested.connect(self.exit_requested)

    def confirm_exit(self) -> bool:
        logging.info("Exit confirmation requested")
        # Place for any final checks (e.g. asking the user whether results of the work should be saved).
        return True

    def quit(self) -> None:
        self.main_window.close()


class ExecutorWithExitChecks(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        # QApplication instance should exist before any Qt features are used, so Executor is created first.
        self._orchestrator: Orchestrator | None = None

    def set_orchestrator(self, orchestrator: Orchestrator) -> None:
        self._orchestrator = orchestrator
        self._orchestrator.exit_requested.connect(self.on_exit_requested)

    @Slot()
    def on_exit_requested(self):
        if not self._orchestrator.confirm_exit():
            return
        self._orchestrator.quit()
        self.quit()


if __name__ == "__main__":  # pragma: no cover
    executor = ExecutorWithExitChecks()
    executor.set_orchestrator(Orchestrator())
    sys.exit(executor.exec())
