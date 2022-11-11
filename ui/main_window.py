import sys

from PySide6.QtCore import Slot, QSize, QPoint, QRect
from PySide6.QtWidgets import QMainWindow, QFileDialog, QApplication

from app.data import Deck, AnkiIO, DeckJsonIO, Path, Settings, StoredSettings
from app.info import PROJECT_FULL_NAME, PROJECT_NAME
from ui.app_status_bar import AppStatusBar
from ui.gen.main_window_uic import Ui_MainWindow
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
        if Settings.get(StoredSettings.IMPORT_ON_STARTUP):
            self.open_deck_file(Settings.get(StoredSettings.LAST_PROJECT_FILE_PATH))

        # TODO
        # self.table_model = SummaryCardsModel(self.current_deck)
        # self.table_view = CardsTableView(self, self.table_model)
        # self.ui.main_layout.replaceWidget(self.ui.cards_table_view_placeholder, self.table_view)
        # self.ui.cards_table_view_placeholder.setParent(None)
        # self.ui.cards_table_view_placeholder.deleteLater()

        self.show()

        self.restore_window_geometry()

    def restore_window_geometry(self):
        min_size: QSize = self.minimumSize()
        window_geometry: QRect = Settings.get(StoredSettings.MAIN_WINDOW_GEOMETRY)

        # At least 100px x 100px top-left part of the window is visible on any of the screens.
        def top_left_corner_visible(screen_rect: QRect):
            return screen_rect.contains(window_geometry.topLeft()) and \
                   screen_rect.contains(window_geometry.topLeft() + QPoint(100, 100))

        if any((top_left_corner_visible(screen.geometry()) for screen in QApplication.screens())):
            self.setGeometry(window_geometry)
        else:
            current_screen = self.screen().geometry()
            half_min_size: QPoint = QPoint(min_size.width() / 2, min_size.height() / 2)
            geometry = QRect(current_screen.center() - half_min_size, min_size)
            self.setGeometry(QRect(current_screen.center() - half_min_size, min_size))

        # self.table_view.restore_geometry()

    def store_window_geometry(self):
        # self.table_view.store_geometry()
        Settings.set(StoredSettings.MAIN_WINDOW_GEOMETRY, self.geometry())

    @Slot(ShortcutCommand)
    def on_shortcut_activated(self, shortcut_command: ShortcutCommand):
        if shortcut_command == ShortcutCommand.SUGGEST:
            self.lookup_and_suggest()
        # self.table_view.execute_shortcut_action(shortcut_command)

    def lookup_and_suggest(self):
        pass
        # lookup_data = self.table_view.lookup_data_in_focus()
        # if lookup_data is None:
        #     return
        # suggestions = Lookup.suggestions(lookup_data)
        # suggestions.append(self.table_view.selected_card())
        # lookup_model = LookupCardsModel(suggestions, self.table_model)
        # self.lookup_dialog = LookupDialog(self, lookup_model)
        # self.lookup_dialog.adjust_to_row(self.table_view.selected_card_rect(), self.table_view.get_header_sizes())
        # self.lookup_dialog.exec() # Replace with open/finished
        # self.lookup_dialog = None

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

    def set_deck_name_as(self, name: str):
        new_name = name.strip()
        if not new_name:
            new_name = 'New Deck'
        self.current_deck.deck_name = new_name
        self.ui.deck_name.setText(new_name)
