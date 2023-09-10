from PySide6.QtCore import QObject, Slot
from PySide6.QtWidgets import QMainWindow, QFileDialog

from core.files import anki as anki_io
from core.files import deck_json as deck_io
from core.info import PROJECT_NAME
from core.settings import Settings, StoredSettings
from core.types import Deck
from core.util import UniversalPath, Status
from ui.main_window.controllers.deck_controller import DeckController
from ui.main_window.main_window import MainWindow


class FileController(QObject):
    def __init__(self, parent: QObject, main_window: MainWindow, deck_controller: DeckController):
        super().__init__(parent)
        self.main_window = main_window
        self.deck_controller = deck_controller

        main_window.ui.top_menu_file_new.triggered.connect(self.on_action_new_deck)
        main_window.ui.top_menu_file_open.triggered.connect(self.on_action_open_project)
        main_window.ui.top_menu_file_save.triggered.connect(self.on_action_save_project)
        main_window.ui.top_menu_file_save_as.triggered.connect(self.on_action_save_project_as)
        main_window.ui.top_menu_file_export.triggered.connect(self.on_action_export_deck)

    def _write_deck_file(self, deck: Deck, output_path: UniversalPath) -> Status:
        deck.normalize_for_output()
        status = deck_io.write_file(deck, output_path)
        if status.is_ok():
            Settings.set(StoredSettings.LAST_PROJECT_FILE_PATH, str(output_path))
            deck.file_path = output_path
            self.deck_controller.mark_deck_saved()
            self.deck_controller.update_deck_meta()
        return status

    def try_open_deck_file(self, input_path: UniversalPath) -> bool:
        if not input_path.exists():
            self._show_status('File {} does not exist')
            return False
        reading_status = deck_io.read_file(input_path)
        if not reading_status.is_ok():
            self._show_status(reading_status.status)
            return False
        Settings.set(StoredSettings.LAST_PROJECT_FILE_PATH, str(input_path))
        self.deck_controller.reset_deck(reading_status.value)
        return True

    @staticmethod
    def startup_deck() -> Deck:
        startup_deck_path = Settings.get(StoredSettings.LAST_PROJECT_FILE_PATH)
        if startup_deck_path:
            startup_deck_status = deck_io.read_file(UniversalPath(startup_deck_path))
            if startup_deck_status.is_ok():
                return startup_deck_status.value
        return DeckController.default_deck()

    @staticmethod
    def _ask_user_for_deck_file_path(dialog_parent: QMainWindow) -> UniversalPath | None:
        raw_dialog_result = QFileDialog.getSaveFileName(dialog_parent, "Save as {} deck file...".format(PROJECT_NAME),
                                                        dir=Settings.get(StoredSettings.LAST_PROJECT_FILE_PATH),
                                                        filter="Deck JSON (*.json)")
        if raw_dialog_result[0]:
            # Enforce correct file extension
            return UniversalPath(raw_dialog_result[0]).with_extension('.json')
        return None

    def _show_status(self, new_status: str):
        self.main_window.status_bar.show_timed_message(new_status)

    def _deck(self):
        return self.deck_controller.deck

    @Slot()
    def on_action_new_deck(self):
        self.main_window.overview_table_view.commit_open_editor_changes()
        # TODO: Check if current deck needs to be saved
        self.deck_controller.reset_deck(self.deck_controller.default_deck())

    @Slot()
    def on_action_open_project(self):
        self.main_window.overview_table_view.commit_open_editor_changes()
        # TODO: Check if current deck needs to be saved
        raw_dialog_result = QFileDialog.getOpenFileName(self.main_window, "Open {} deck file...".format(PROJECT_NAME),
                                                        dir=Settings.get(StoredSettings.LAST_PROJECT_FILE_PATH),
                                                        filter="Deck JSON (*.json)")
        if raw_dialog_result[0]:
            input_path = UniversalPath(raw_dialog_result[0]).with_extension('.json')
            self.try_open_deck_file(input_path)
        else:
            self._show_status('No path selected to the deck file')

    @Slot()
    def on_action_save_project(self) -> bool:
        self.main_window.overview_table_view.commit_open_editor_changes()
        if self._deck().file_path is not None:
            writing_status = self._write_deck_file(self._deck(), self._deck().file_path)
            if writing_status.is_ok():
                return True
            else:
                self._show_status(writing_status.status)
        return self.on_action_save_project_as()

    @Slot()
    def on_action_save_project_as(self) -> bool:
        self.main_window.overview_table_view.commit_open_editor_changes()
        if output_path := self._ask_user_for_deck_file_path(self.main_window):
            writing_status = self._write_deck_file(self.main_window.overview_model.deck, output_path)
            if writing_status.is_ok():
                self._deck().file_path = output_path
                return True
            else:
                self._show_status(writing_status.status)
                return False
        else:
            self._show_status('No output path chosen for deck project file')
            return False

    @Slot()
    def on_action_export_deck(self):
        self.main_window.overview_table_view.commit_open_editor_changes()
        raw_dialog_result = QFileDialog.getSaveFileName(self.main_window, "Save as Anki project file...",
                                                        dir=Settings.get(StoredSettings.LAST_ANKI_FILE_PATH),
                                                        filter="Anki project package (*.apkg)")
        if not raw_dialog_result[0]:
            self._show_status('No output path for Anki file')
            return
        output_path = UniversalPath(raw_dialog_result[0]).with_extension('.apkg')

        self._deck().normalize_for_output()
        self.deck_controller.update_deck_meta()
        writing_status = anki_io.write_file(self._deck(), output_path)
        if writing_status.is_ok():
            Settings.set(StoredSettings.LAST_ANKI_FILE_PATH, str(output_path))
        else:
            self._show_status(writing_status.status)
