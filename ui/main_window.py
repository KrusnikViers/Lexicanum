import sys

from PySide6.QtCore import Slot, QSize, QPoint, QRect
from PySide6.QtWidgets import QMainWindow, QFileDialog

from app.data.deck import Deck
from app.data.storage.anki import AnkiIO
from app.data.storage.deck_json import DeckJsonIO
from app.data.storage.path import Path
from app.data.storage.settings import Settings, StoredSettings
from app.info import PROJECT_FULL_NAME, PROJECT_NAME
from app.translation_lookup.lookup import Lookup
from ui.app_status_bar import AppStatusBar
from ui.cards_table.model.lookup import LookupCardsModel
from ui.cards_table.model.summary import SummaryCardsModel
from ui.cards_table.view import CardsTableView
from ui.gen.main_window_uic import Ui_MainWindow
from ui.lookup_dialog import LookupDialog
from ui.shared.shortcuts import Shortcuts, ShortcutCommand


class MainWindow(QMainWindow):
    def closeEvent(self, _) -> None:
        self.store_window_geometry()
        sys.exit(0)

    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(PROJECT_FULL_NAME)

        self.shortcuts = Shortcuts(self)
        self.shortcuts.activated.connect(self.on_shortcut_activated)

        self.status_bar = AppStatusBar(self)
        self.setStatusBar(self.status_bar)

        self.current_deck = Deck('New Deck', [])
        self.was_changed = False
        if Settings.get(StoredSettings.IMPORT_ON_STARTUP):
            self.open_deck_file(Settings.get(StoredSettings.LAST_PROJECT_FILE_PATH))

        self.table_model = SummaryCardsModel(self.current_deck)
        self.table_view = CardsTableView(self, self.table_model)
        self.ui.main_layout.replaceWidget(self.ui.cards_table_view_placeholder, self.table_view)
        self.ui.cards_table_view_placeholder.setParent(None)
        self.ui.cards_table_view_placeholder.deleteLater()

        self.lookup_dialog: LookupDialog | None = None

        self.update_state_on_deck_metadata_changed()
        self.connect_all()
        self.show()

        self.restore_window_geometry()

    def connect_all(self):
        self.ui.deck_open.clicked.connect(self.on_deck_open)
        self.ui.deck_save.clicked.connect(self.on_deck_save)
        self.ui.deck_save_as.clicked.connect(self.on_deck_save_as)
        self.ui.deck_export_anki.clicked.connect(self.on_deck_export_anki)
        self.ui.deck_name.textChanged.connect(self.update_state_on_deck_metadata_changed)

    def restore_window_geometry(self):
        min_size: QSize = self.minimumSize()
        geometry: QRect = Settings.get(StoredSettings.MAIN_WINDOW_GEOMETRY)
        screen = self.screen().availableGeometry()

        min_size_enough = geometry.width() >= min_size.width() and geometry.height() >= min_size.height()
        if not screen.contains(geometry) or not min_size_enough:
            print('Screen geometry is wrong ({} is outside the screen {} or less than {}), restoring default'.format(
                geometry, screen, min_size))
            half_min_size: QPoint = QPoint(min_size.width() / 2, min_size.height() / 2)
            geometry = QRect(screen.center() - half_min_size, min_size)
        self.setGeometry(geometry)
        self.table_view.restore_geometry()

    def store_window_geometry(self):
        self.table_view.store_geometry()
        Settings.set(StoredSettings.MAIN_WINDOW_GEOMETRY, self.geometry())

    @Slot()
    def update_state_on_deck_metadata_changed(self):
        if self.ui.deck_name.text().strip() != self.current_deck.deck_name:
            self.was_changed = True
        self.ui.deck_save.setVisible(self.current_deck.file_path is not None)
        if self.current_deck.file_path is not None:
            saved_status = 'Unsaved changes in ' if self.was_changed else ''
            message = '{}{} (id{}), {}'.format(
                saved_status, self.current_deck.deck_name,
                self.current_deck.deck_id, self.current_deck.file_path.as_str())
        else:
            message = 'Creating brand new deck'
        self.status_bar.show_message(message)

    @Slot(ShortcutCommand)
    def on_shortcut_activated(self, shortcut_command: ShortcutCommand):
        if shortcut_command == ShortcutCommand.SUGGEST and self.lookup_dialog is None:
            self.lookup_and_suggest()

        if shortcut_command != ShortcutCommand.SUGGEST:
            self.table_view.shortcut_action(shortcut_command)

    def lookup_and_suggest(self):
        lookup_data = self.table_view.lookup_data_in_focus()
        if lookup_data is None:
            return
        suggestions = Lookup.suggestions(lookup_data)
        suggestions.append(self.table_view.selected_card())
        lookup_model = LookupCardsModel(suggestions, self.table_model)
        self.lookup_dialog = LookupDialog(self, lookup_model)
        self.lookup_dialog.adjust_to_row(self.table_view.selected_card_rect(), self.table_view.get_header_sizes())
        self.lookup_dialog.exec()
        self.lookup_dialog = None

    # Deck files operations
    ####################################################################################################################
    @Slot()
    def on_deck_save_as(self):
        file_search_result = QFileDialog.getSaveFileName(self, "Save as {} deck file...".format(PROJECT_NAME),
                                                         dir=Settings.get(StoredSettings.LAST_PROJECT_FILE_PATH),
                                                         filter="Deck JSON (*.json)")
        if file_search_result[0]:
            raw_output_path = Path(file_search_result[0])
            self.on_deck_save(raw_output_path)

    @Slot()
    def on_deck_save(self, raw_output_path: Path | None = None):
        self.set_deck_name_as(self.ui.deck_name.text())
        self.current_deck.normalize_for_output()

        output_path = raw_output_path if raw_output_path else self.current_deck.file_path
        status = DeckJsonIO.write_to_file(self.current_deck, output_path)
        if not status.is_ok():
            self.status_bar.show_timed_message(status.status)
            return
        Settings.set(StoredSettings.LAST_PROJECT_FILE_PATH, output_path.as_str())
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

        output_path = Path(file_search_result[0])
        status = AnkiIO.write_to_file(self.current_deck, output_path)
        if not status.is_ok():
            self.status_bar.show_timed_message(status.status)
            return
        Settings.set(StoredSettings.LAST_ANKI_FILE_PATH, output_path.as_str())
        self.update_state_on_deck_metadata_changed()

    @Slot()
    def on_deck_open(self):
        file_search_result = QFileDialog.getOpenFileName(self, "Open {} deck file...".format(PROJECT_NAME),
                                                         dir=Settings.get(StoredSettings.LAST_PROJECT_FILE_PATH),
                                                         filter="Deck JSON (*.json)")
        if not file_search_result[0]:
            return
        self.open_deck_file(file_search_result[0])

    def open_deck_file(self, raw_file_path: str):
        input_path = Path(raw_file_path)
        if not input_path.exists():
            self.status_bar.show_timed_message('{} not read: does not exist'.format(input_path.as_str()))
            return
        result = DeckJsonIO.read_from_file(input_path)
        if not result.is_ok():
            self.status_bar.show_timed_message(result.status)
            return
        Settings.set(StoredSettings.LAST_PROJECT_FILE_PATH, input_path.as_str())
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
