import sys

from PySide6.QtCore import Qt, Slot, QSize, QPoint, QRect
from PySide6.QtGui import QFontMetrics
from PySide6.QtWidgets import QMainWindow, QApplication

from core.info import PROJECT_FULL_NAME
from core.settings import Settings, StoredSettings
from core.types import Deck
from core.util import Status, UniversalPath
from ui.common import IconsList
from ui.common import Shortcuts, ShortcutCommand
from ui.gen.main_window.main_window_uic import Ui_MainWindow
from ui.main_window.input_table import InputCardsTableView, InputCardsTableModel
from ui.main_window.operations import files as deck_io
from ui.main_window.overview_table import OverviewCardsTableView, OverviewCardsTableModel
from ui.main_window.widgets import AppStatusBar


class MainWindow(QMainWindow):
    def closeEvent(self, _) -> None:
        self.store_window_geometry()
        sys.exit(0)

    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(PROJECT_FULL_NAME)

        self.shortcuts: Shortcuts = Shortcuts(self)
        self.shortcuts.activated.connect(self.on_shortcut_activated)

        self.status_bar: AppStatusBar = AppStatusBar(self)
        self.setStatusBar(self.status_bar)

        self.overview_model = OverviewCardsTableModel(self.get_default_deck(on_startup=True))
        self.overview_model.deck_updated.connect(self.on_deck_info_updated)
        self.overview_table_view = OverviewCardsTableView(self, self.overview_model)
        self.ui.main_layout.replaceWidget(self.ui.cards_table_view_placeholder, self.overview_table_view)
        self.ui.cards_table_view_placeholder.setParent(None)
        self.ui.cards_table_view_placeholder.deleteLater()

        self.input_model = InputCardsTableModel()
        self.input_model.dataChanged.connect(self.reset_overview_filter)
        self.input_table_view = InputCardsTableView(self, self.input_model)
        self.ui.main_layout.replaceWidget(self.ui.input_table_view_placeholder, self.input_table_view)
        self.ui.input_table_view_placeholder.setParent(None)
        self.ui.input_table_view_placeholder.deleteLater()
        self.input_table_view.horizontalHeader().sectionResized.connect(self.sync_tables_geometry)

        self.ui.deck_name.setText(self.overview_model.deck.deck_name)
        self.ui.deck_name.textChanged.connect(self.on_deck_name_changed)
        self.on_deck_info_updated()

        self.ui.menu_toggle_sidebar.setIcon(IconsList.Sidebar)
        self.ui.tbutton_toggle_sidebar.setDefaultAction(self.ui.menu_toggle_sidebar)
        self.ui.menu_toggle_sidebar.triggered.connect(self.action_toggle_sidebar)

        self.ui.menu_new.triggered.connect(self.action_new_deck)
        self.ui.menu_open.triggered.connect(self.action_open_project)
        self.ui.menu_save.triggered.connect(self.action_save_project)
        self.ui.menu_save_as.triggered.connect(self.action_save_project_as)
        self.ui.menu_export.triggered.connect(self.action_export_deck)

        self.show()
        self.restore_window_geometry()

    def get_default_deck(self, on_startup: bool) -> Deck:
        if on_startup and Settings.get(StoredSettings.IMPORT_ON_STARTUP):
            import_file_path = UniversalPath(Settings.get(StoredSettings.LAST_PROJECT_FILE_PATH))
            import_status = deck_io.read_deck_file(import_file_path)
            if import_status.is_ok():
                return import_status.value
            else:
                self.status_bar.show_timed_message(import_status.status)
        return Deck('New Deck', [])

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
            self.setGeometry(QRect(current_screen.center() - half_min_size, min_size))

        is_sidebar_visible = Settings.get(StoredSettings.SIDEBAR_VISIBLE)
        self.ui.right_sidebar.setVisible(is_sidebar_visible)
        self.ui.menu_toggle_sidebar.setChecked(is_sidebar_visible)

        self.input_table_view.restore_geometry()
        self.sync_tables_geometry()

    def store_window_geometry(self):
        self.input_table_view.store_geometry()
        Settings.set(StoredSettings.MAIN_WINDOW_GEOMETRY, self.geometry())
        Settings.set(StoredSettings.SIDEBAR_VISIBLE, self.ui.right_sidebar.isVisible())

    @Slot(str)
    def on_deck_name_changed(self, new_name: str):
        self.overview_model.deck.deck_name = new_name
        self.overview_model.deck.was_updated = True
        self.on_deck_info_updated()

    @Slot()
    def on_deck_reset(self):
        deck = self.overview_model.deck
        self.ui.deck_name.setText(deck.deck_name)
        self.on_deck_info_updated()

    @Slot()
    def on_deck_info_updated(self):
        deck = self.overview_model.deck

        # Adjust deck name edit width
        font_metrics = QFontMetrics(self.ui.deck_name.font())
        pixels_width = font_metrics.size(Qt.TextFlag.TextSingleLine, deck.deck_name, tabstops=0).width() + 20
        max_size = self.width() // 3
        pixels_width = max(200, min(max_size, pixels_width))
        self.ui.deck_name.setFixedWidth(pixels_width)

        # Update status message
        cards_count = '{} cards'.format(len(deck.cards))
        save_status = 'not yet saved anywhere' if deck.file_path is None else \
            'changed from {}'.format(deck.file_path) if deck.was_updated else 'saved in {}'.format(deck.file_path)
        self.ui.deck_info.setText('{}, {}'.format(cards_count, save_status))

    @Slot()
    def sync_tables_geometry(self):
        new_header_sizes = self.input_table_view.header_sizes()
        self.overview_table_view.set_header_sizes(new_header_sizes)
        # TODO: Sync horizontal scrolling as well.

    @Slot()
    def reset_overview_filter(self):
        self.overview_model.refresh_displayed_rows(self.input_model.get_input_card())

    @Slot(ShortcutCommand)
    def on_shortcut_activated(self, shortcut_command: ShortcutCommand):
        worst_status = next((status for status in (
            self.input_table_view.maybe_execute_shortcut(shortcut_command),
            self.overview_table_view.maybe_execute_shortcut(shortcut_command)
        ) if not status.is_ok()), Status())
        if not worst_status.is_ok():
            self.status_bar.show_timed_message(worst_status.status)

    @Slot()
    def action_toggle_sidebar(self):
        self.ui.right_sidebar.setVisible(not self.ui.right_sidebar.isVisible())
        self.ui.menu_toggle_sidebar.setChecked(self.ui.right_sidebar.isVisible())

    @Slot()
    def action_new_deck(self):
        # TODO: Save prompt
        self.overview_model.reset_deck(self.get_default_deck(on_startup=False))
        self.on_deck_reset()

    @Slot()
    def action_open_project(self):
        # TODO: Save prompt
        status_or = deck_io.read_deck_file_with_dialog(self)
        if status_or.is_ok():
            self.overview_model.reset_deck(status_or.value)
            self.on_deck_reset()
        else:
            self.status_bar.show_timed_message(status_or.status)

    def on_deck_write(self, status: Status):
        if status.is_ok():
            self.overview_model.deck.was_updated = False
            self.on_deck_reset()
        else:
            self.status_bar.show_timed_message(status.status)

    @Slot()
    def action_save_project(self):
        self.on_deck_write(deck_io.write_deck_file(self, self.overview_model.deck))

    @Slot()
    def action_save_project_as(self):
        self.on_deck_write(deck_io.write_deck_file_with_dialog(self, self.overview_model.deck))

    @Slot()
    def action_export_deck(self):
        self.on_deck_write(deck_io.write_apkg_with_dialog(self, self.overview_model.deck))

    # @Slot(CardsModelHeader, str)
    # def lookup_and_suggest(self, column: CardsModelHeader, request: str):
    #     pass  # TODO
    # lookup_data = LookupData(request, Language.DE if column == CardsModelHeader.Question else Language.EN)
    # suggestions = Lookup.suggestions(lookup_data)
    # suggestions.append(self.input_model.get_input_card())
    # lookup_model = LookupCardsModel(suggestions)
    # lookup_dialog = LookupDialog(self, self.status_bar, lookup_model, self.overview_model)
    # lookup_dialog.exec()
