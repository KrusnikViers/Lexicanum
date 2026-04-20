import unittest

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from main import ExecutorWithExitChecks, Orchestrator


def _force_quit():
    QApplication.exit(1)


class MainApplicationTest(unittest.TestCase):

    def test_main_starts_and_finishes(self):
        executor = ExecutorWithExitChecks()
        orchestrator = Orchestrator()

        executor.set_orchestrator(orchestrator)

        def _simulate_normal_close():
            orchestrator.main_window.close()

        QTimer.singleShot(500, _simulate_normal_close)
        QTimer.singleShot(1000, _force_quit)

        return_code = executor.exec()
        self.assertEqual(return_code, 0)
