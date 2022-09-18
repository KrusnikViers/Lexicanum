import sys
from pathlib import Path

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog

from app.data.deck import Deck
from app.data.storage.anki import AnkiIO
from app.data.storage.deck_json import DeckJsonIO
from app.data.storage.settings import Settings, StoredSettings
from app.info import PROJECT_FULL_NAME, PROJECT_NAME
from ui.app_status_bar import AppStatusBar
from ui.cards_table_model import CardsTableModel
from ui.cards_table_view import CardsTableView
from ui.gen.main_window_uic import Ui_MainWindow


class MainWindow(QMainWindow):
    def closeEvent(self, _) -> None:
        sys.exit(0)

    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(PROJECT_FULL_NAME)
        # Disable "help" button on the top panel - context prompts are not supported.
        self.restore_window_geometry()

        self.status_bar = AppStatusBar(self)
        self.setStatusBar(self.status_bar)

        self.current_deck = Deck('New Deck', [])
        self.was_changed = False
        if Settings.get(StoredSettings.IMPORT_ON_STARTUP):
            self.open_deck_file(Settings.get(StoredSettings.LAST_PROJECT_FILE_PATH))

        self.table_model = CardsTableModel(self.current_deck)
        self.table_view = CardsTableView(self, self.table_model)
        self.ui.cards_table_view_placeholder.deleteLater()
        self.ui.main_layout.replaceWidget(self.ui.cards_table_view_placeholder, self.table_view)

        self.update_state_on_deck_metadata_changed()
        self.connect_all()
        self.show()

    def connect_all(self):
        self.ui.deck_open.clicked.connect(self.on_deck_open)
        self.ui.deck_save.clicked.connect(self.on_deck_save)
        self.ui.deck_save_as.clicked.connect(self.on_deck_save_as)
        self.ui.deck_export_anki.clicked.connect(self.on_deck_export_anki)
        self.ui.deck_name.textChanged.connect(self.update_state_on_deck_metadata_changed)

    # Window appearance
    ####################################################################################################################
    def restore_window_geometry(self):
        pass  # TODO

    def store_window_geometry(self):
        pass  # TODO

    @Slot()
    def update_state_on_deck_metadata_changed(self):
        if self.ui.deck_name.text().strip() != self.current_deck.deck_name:
            self.was_changed = True
        self.ui.deck_save.setVisible(self.current_deck.file_path is not None)
        self.ui.deck_save.setEnabled(self.was_changed)
        if self.current_deck.file_path is not None:
            saved_status = 'Unsaved changes in ' if self.was_changed else ''
            message = '{}{} (id{}), {}'.format(
                saved_status, self.current_deck.deck_name, self.current_deck.deck_id, self.current_deck.file_path)
        else:
            message = 'Creating brand new deck'
        self.status_bar.show_message(message)

    # Deck files operations
    ####################################################################################################################
    @Slot()
    def on_deck_save_as(self):
        file_search_result = QFileDialog.getSaveFileName(self, "Save as {} deck file...".format(PROJECT_NAME),
                                                         dir=Settings.get(StoredSettings.LAST_PROJECT_FILE_PATH),
                                                         filter="Deck JSON (*.json)")
        if file_search_result[0]:
            self.on_deck_save(file_search_result[0])

    @Slot()
    def on_deck_save(self, file_path=None):
        self.set_deck_name_as(self.ui.deck_name.text())
        self.current_deck.normalize_for_output()

        output_path = Path(self.current_deck.file_path if file_path is None else file_path).resolve()
        status = DeckJsonIO.write_to_file(self.current_deck, output_path.with_suffix('.json'))
        if not status.is_ok():
            self.status_bar.show_timed_message(status.status)
            return
        self.current_deck.file_path = output_path
        Settings.set(StoredSettings.LAST_PROJECT_FILE_PATH, output_path)
        self.was_changed = False
        self.update_state_on_deck_metadata_changed()

    @Slot()
    def on_deck_export_anki(self):
        file_search_result = QFileDialog.getSaveFileName(self, "Save as Anki project file...",
                                                         dir=Settings.get(StoredSettings.LAST_ANKI_FILE_PATH),
                                                         filter="Anki project package (*.apkg)")
        if not file_search_result[0]:
            return
        self.set_deck_name_as(self.ui.deck_name.text())
        self.current_deck.normalize_for_output()

        output_path = Path(file_search_result[0]).resolve()
        status = AnkiIO.write_to_file(self.current_deck, output_path.with_suffix('.apkg'))
        if not status.is_ok():
            self.status_bar.show_timed_message(status.status)
            return
        Settings.set(StoredSettings.LAST_ANKI_FILE_PATH, output_path)
        self.update_state_on_deck_metadata_changed()

    @Slot()
    def on_deck_open(self):
        file_search_result = QFileDialog.getOpenFileName(self, "Open {} deck file...".format(PROJECT_NAME),
                                                         dir=Settings.get(StoredSettings.LAST_PROJECT_FILE_PATH),
                                                         filter="Deck JSON (*.json)")
        if not file_search_result[0]:
            return
        self.open_deck_file(file_search_result[0])

    def open_deck_file(self, file_path: str):
        result = DeckJsonIO.read_from_file(Path(file_path))
        if not result.is_ok():
            self.status_bar.show_timed_message(result.status)
            return
        Settings.set(StoredSettings.LAST_PROJECT_FILE_PATH, file_path)
        self.current_deck = result.value
        self.set_deck_name_as(self.current_deck.deck_name)
        self.was_changed = False
        self.update_state_on_deck_metadata_changed()

    def set_deck_name_as(self, name: str):
        new_name = name.strip()
        if not new_name:
            new_name = 'New Deck'
        self.current_deck.deck_name = new_name
        self.ui.deck_name.setText(new_name)
