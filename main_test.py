import unittest

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from main import Application


def _simulate_normal_close():
    app = Application.get_or_create()
    app.main_window.close()


def _force_quit():
    QApplication.exit(1)


class MainApplicationTest(unittest.TestCase):

    def test_main_starts_and_finishes(self):
        # Create an App early for timers to latch on.
        app = Application.get_or_create()
        QTimer.singleShot(500, _simulate_normal_close)
        QTimer.singleShot(1000, _force_quit)

        return_code = app.exec()
        self.assertEqual(return_code, 0)
