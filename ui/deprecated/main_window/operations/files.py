from PySide6.QtWidgets import QMainWindow, QFileDialog

from core.files import anki as anki_io
from core.files import deck_json as deck_io
from core.info import PROJECT_NAME
from core.settings import Settings, StoredSettings
from core.types import Deck
from core.util import UniversalPath, Status, StatusOr


def _write_deck_file(deck: Deck, output_path: UniversalPath):
    deck.normalize_for_output()
    status = deck_io.write_file(deck, output_path)
    if status:
        Settings.set(StoredSettings.LAST_PROJECT_FILE_PATH, str(output_path))
    return status


def _ask_user_for_deck_file_path(dialog_parent: QMainWindow) -> UniversalPath | None:
    raw_dialog_result = QFileDialog.getSaveFileName(dialog_parent, "Save as {} deck file...".format(PROJECT_NAME),
                                                    dir=Settings.get(StoredSettings.LAST_PROJECT_FILE_PATH),
                                                    filter="Deck JSON (*.json)")
    if raw_dialog_result[0]:
        # Enforce correct file extension
        return UniversalPath(raw_dialog_result[0]).with_extension('.json')
    return None


def write_deck_file_with_dialog(dialog_parent: QMainWindow, deck: Deck) -> Status:
    if output_path := _ask_user_for_deck_file_path(dialog_parent):
        status = _write_deck_file(deck, output_path)
        if status:
            deck.file_path = output_path
        return status
    return Status('No output path for deck file')


def write_deck_file(dialog_parent: QMainWindow, deck: Deck) -> Status:
    if deck.file_path is not None:
        return _write_deck_file(deck, deck.file_path)
    return write_deck_file_with_dialog(dialog_parent, deck)


def write_apkg_with_dialog(dialog_parent: QMainWindow, deck: Deck) -> Status:
    raw_dialog_result = QFileDialog.getSaveFileName(dialog_parent, "Save as Anki project file...",
                                                    dir=Settings.get(StoredSettings.LAST_ANKI_FILE_PATH),
                                                    filter="Anki project package (*.apkg)")
    if not raw_dialog_result[0]:
        return Status('No output path for Anki file')
    output_path = UniversalPath(raw_dialog_result[0]).with_extension('.apkg')

    deck.normalize_for_output()
    status = anki_io.write_file(deck, output_path)
    if status:
        return status
    Settings.set(StoredSettings.LAST_ANKI_FILE_PATH, str(output_path))


def read_deck_file(input_path: UniversalPath) -> StatusOr[Deck]:
    if not input_path.exists():
        return StatusOr(status='File {} does not exist'.format(input_path))
    status = deck_io.read_file(input_path)
    if status:
        Settings.set(StoredSettings.LAST_PROJECT_FILE_PATH, str(input_path))
    return status


def read_deck_file_with_dialog(dialog_parent: QMainWindow) -> StatusOr[Deck]:
    raw_dialog_result = QFileDialog.getOpenFileName(dialog_parent, "Open {} deck file...".format(PROJECT_NAME),
                                                    dir=Settings.get(StoredSettings.LAST_PROJECT_FILE_PATH),
                                                    filter="Deck JSON (*.json)")
    if raw_dialog_result[0]:
        input_path = UniversalPath(raw_dialog_result[0]).with_extension('.json')
        return read_deck_file(input_path)
    return StatusOr(status='No path to the deck file')
