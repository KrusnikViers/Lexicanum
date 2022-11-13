from PySide6.QtWidgets import QMainWindow, QFileDialog

from app.data import Deck, AnkiIO, DeckJsonIO, Path, Settings, StoredSettings
from app.data.base.status_or import Status, StatusOr
from app.info import PROJECT_NAME


class FileOperationsHelper:
    @staticmethod
    def _save_deck_to(deck: Deck, output_path: Path) -> Status:
        deck.normalize_for_output()
        status = DeckJsonIO.write_to_file(deck, output_path)
        if status.is_ok():
            Settings.set(StoredSettings.LAST_PROJECT_FILE_PATH, output_path.as_str())
        return status

    @staticmethod
    def _ask_path_to_save_deck(dialog_parent: QMainWindow) -> Path | None:
        file_search_result = QFileDialog.getSaveFileName(dialog_parent, "Save as {} deck file...".format(PROJECT_NAME),
                                                         dir=Settings.get(StoredSettings.LAST_PROJECT_FILE_PATH),
                                                         filter="Deck JSON (*.json)")
        return Path(file_search_result[0]) if file_search_result[0] else None

    @classmethod
    def save_deck_select(cls, dialog_parent: QMainWindow, deck: Deck) -> Status:
        if output_path := cls._ask_path_to_save_deck(dialog_parent):
            return cls._save_deck_to(deck, output_path)
        return Status.from_status('Output project file not selected')

    @classmethod
    def save_deck(cls, dialog_parent: QMainWindow, deck: Deck) -> Status:
        if deck.file_path is not None:
            return cls._save_deck_to(deck, deck.file_path)
        elif output_path := cls._ask_path_to_save_deck(dialog_parent):
            status = cls._save_deck_to(deck, output_path)
            if status.is_ok():
                deck.file_path = output_path
            return status
        return Status.from_status('Output project file not selected')

    @staticmethod
    def export_deck_select(dialog_parent: QMainWindow, deck: Deck) -> Status:
        file_search_result = QFileDialog.getSaveFileName(dialog_parent, "Save as Anki project file...",
                                                         dir=Settings.get(StoredSettings.LAST_ANKI_FILE_PATH),
                                                         filter="Anki project package (*.apkg)")
        if not file_search_result[0]:
            return Status.from_status('Output Anki file not selected')
        output_path = Path(file_search_result[0])
        deck.normalize_for_output()

        status = AnkiIO.write_to_file(deck, output_path)
        if status.is_ok():
            Settings.set(StoredSettings.LAST_ANKI_FILE_PATH, output_path.as_str())
        return status

    @classmethod
    def open_deck_select(cls, dialog_parent: QMainWindow) -> StatusOr[Deck]:
        file_search_result = QFileDialog.getOpenFileName(dialog_parent, "Open {} deck file...".format(PROJECT_NAME),
                                                         dir=Settings.get(StoredSettings.LAST_PROJECT_FILE_PATH),
                                                         filter="Deck JSON (*.json)")
        if not file_search_result[0]:
            return StatusOr.from_status('Project file not selected')
        return cls.open_deck(Path(file_search_result[0]))

    @staticmethod
    def open_deck(input_path: Path) -> StatusOr[Deck]:
        if not input_path.exists():
            return StatusOr.from_status('File {} does not exist'.format(input_path.as_str()))
        status = DeckJsonIO.read_from_file(input_path)
        if status.is_ok():
            Settings.set(StoredSettings.LAST_PROJECT_FILE_PATH, input_path.as_str())
        return status
