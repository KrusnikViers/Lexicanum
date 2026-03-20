import unittest

from PySide6.QtWidgets import QWidget

from ui.main_window import status_bar


class TestStatusBar(unittest.TestCase):
    def setUp(self):
        self.parent = QWidget()
        self.bar = status_bar.StatusBar(self.parent)

    def test_set_different_css_for_different_styles(self):
        self.bar.set_temporary_status('Status')
        usual_style = self.bar._ui_status_label.styleSheet()
        self.bar.set_temporary_status('Error', status_type=status_bar.StatusType.Error)
        self.assertNotEqual(usual_style, self.bar._ui_status_label.styleSheet())

    def test_message_resets_on_timer(self):
        self.bar.set_status('Status')
        self.bar.set_temporary_status('Temporary status')
        self.assertEqual(self.bar._ui_status_label.text(), 'Temporary status')
        self.bar._reset_on_timer()
        self.assertEqual(self.bar._ui_status_label.text(), 'Status')
