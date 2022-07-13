import json
import sys

import requests
from PySide2.QtWidgets import QMainWindow

from core.api_info import API_BASE_URI, API_CLIENT_KEY
from core.project_info import PROJECT_FULL_NAME
from ui.gen.main_window_uic import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(PROJECT_FULL_NAME)

        self.ui.lookup.pressed.connect(self.lookup)

    def get_translation(self, lang_pair: str) -> str:
        return requests.get(url='{}/{}'.format(API_BASE_URI, 'lookup'), params={
            'key': API_CLIENT_KEY,
            'lang': lang_pair,
            'text': self.ui.word_input.text()
        }).text

    @staticmethod
    def pretty_print_json(source: str) -> str:
        return json.dumps(json.loads(source), indent=2, sort_keys=True)

    def lookup(self):
        result = '{}\n\n{}'.format(
            self.pretty_print_json(self.get_translation('de-de')),
            self.pretty_print_json(self.get_translation('de-en'))
        )
        self.ui.test_output_label.setText(result)

    def closeEvent(self, _) -> None:
        sys.exit(0)
