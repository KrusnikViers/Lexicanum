import sys
from pathlib import Path

from PySide2.QtCore import Qt, QTimer
from PySide2.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog

from app.data.deck import Deck
from app.data.storage.deck_json import DeckJsonWriter
from app.data.storage.settings import Settings, StoredSettings
from app.info import PROJECT_FULL_NAME, PROJECT_NAME
from ui.gen.main_window_uic import Ui_MainWindow


class _TableIndex:
    Type = 0
    Question = 1
    Answer = 2
    Note = 3


class MainWindow(QMainWindow):
    def closeEvent(self, _) -> None:
        sys.exit(0)

    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(PROJECT_FULL_NAME)
        # Disable "help" button on the top panel - context prompts are not supported.
        QApplication.instance().setAttribute(Qt.AA_DisableWindowContextHelpButton)
        self.status_label = QLabel()
        self.ui.app_status_bar.addWidget(self.status_label, stretch=1)
        self.status_bar_timer = QTimer(self)
        self.status_bar_timer.setSingleShot(True)
        self.status_bar_timer.setInterval(5000)
        self.restore_window_geometry()

        self.current_deck = Deck('New Deck', [])
        self.was_changed = False
        if Settings.get(StoredSettings.IMPORT_ON_STARTUP):
            self.open_deck_file(Settings.get(StoredSettings.LAST_PROJECT_FILE_PATH))
        self.update_state_on_deck_metadata_changed()

        self.connect_all()
        self.show()

    def restore_window_geometry(self):
        pass  # TODO

    def store_window_geometry(self):
        pass  # TODO

    def connect_all(self):
        self.ui.deck_open.clicked.connect(self.on_deck_open)
        self.ui.deck_save.clicked.connect(self.on_deck_save)
        self.ui.deck_save_as.clicked.connect(self.on_deck_save_as)
        self.ui.deck_export_anki.clicked.connect(self.on_deck_export_anki)
        self.status_bar_timer.timeout.connect(self.update_status_bar)
        self.ui.deck_name.textChanged.connect(self.update_state_on_deck_metadata_changed)

    def show_status_message(self, message: str):
        self.status_label.setText(message)
        self.status_bar_timer.start()

    def on_deck_open(self):
        file_search_result = QFileDialog.getOpenFileName(self, "Open {} deck file...".format(PROJECT_NAME),
                                                         dir=Settings.get(StoredSettings.LAST_PROJECT_FILE_PATH),
                                                         filter="Deck JSON (*.json)")
        if not file_search_result[0]:
            return
        self.open_deck_file(file_search_result[0])

    def on_deck_save(self):
        if not self.current_deck.file_path:
            self.on_deck_save_as()
            return

        self.current_deck.deck_name = self.ui.deck_name.text().strip()
        if not self.current_deck.deck_name:
            self.current_deck.deck_name = 'New Deck'
        self.current_deck.normalize_for_output()

        output_path = Path(self.current_deck.file_path).resolve()
        DeckJsonWriter.write_to_file(self.current_deck, output_path.with_suffix('.json'))
        self.was_changed = False
        self.update_state_on_deck_metadata_changed()

    def on_deck_save_as(self):
        file_search_result = QFileDialog.getSaveFileName(self, "Save as {} deck file...".format(PROJECT_NAME),
                                                         dir=Settings.get(StoredSettings.LAST_PROJECT_FILE_PATH),
                                                         filter="Deck JSON (*.json)")
        if not file_search_result[0]:
            return
        Settings.set(StoredSettings.LAST_PROJECT_FILE_PATH, file_search_result[0])
        self.current_deck.file_path = file_search_result[0]
        self.on_deck_save()

    def on_deck_export_anki(self):
        pass

    def open_deck_file(self, file_path: str):
        result = DeckJsonWriter.read_from_file(Path(file_path))
        if not result.is_ok():
            self.show_status_message(result.status)
            return
        Settings.set(StoredSettings.LAST_PROJECT_FILE_PATH, file_path)
        self.current_deck = result.value
        self.ui.deck_name.setText(self.current_deck.deck_name)

        self.was_changed = False
        self.update_state_on_deck_metadata_changed()

    def update_state_on_deck_metadata_changed(self):
        if self.ui.deck_name.text().strip() != self.current_deck.deck_name:
            self.was_changed = True
        self.ui.deck_save.setVisible(self.current_deck.file_path is not None)
        self.ui.deck_save.setEnabled(self.was_changed)
        self.update_status_bar()

    def update_status_bar(self):
        if self.status_bar_timer.isActive():
            return
        if self.current_deck.file_path is not None:
            saved_status = 'Unsaved changes in ' if self.was_changed else ''
            message = '{}{} (id{}), {}'.format(
                saved_status, self.current_deck.deck_name, self.current_deck.deck_id, self.current_deck.file_path)
        else:
            message = 'Creating brand new deck'
        self.status_label.setText(message)
