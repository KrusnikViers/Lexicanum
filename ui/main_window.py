import sys

from PySide6.QtCore import Slot, QSize, QPoint, QRect
from PySide6.QtWidgets import QMainWindow, QApplication

from app.data import Deck, Settings, StoredSettings, Path
from app.info import PROJECT_FULL_NAME
from ui.app_status_bar import AppStatusBar
from ui.cards_table import InputCardsTableView, InputCardsModel
from ui.cards_table import SummaryCardsModel, ListingCardsTableView
from ui.files_operations_helper import FileOperationsHelper
from ui.gen.main_window_uic import Ui_MainWindow
from ui.shared.icons.icons import SharedIcons
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

        self.shortcuts: Shortcuts = Shortcuts(self)
        self.shortcuts.activated.connect(self.on_shortcut_activated)

        self.status_bar: AppStatusBar = AppStatusBar(self)
        self.setStatusBar(self.status_bar)

        self.current_deck = Deck('New Deck', [])
        if Settings.get(StoredSettings.IMPORT_ON_STARTUP):
            import_file_path = Path(Settings.get(StoredSettings.LAST_PROJECT_FILE_PATH))
            import_status = FileOperationsHelper.open_deck(import_file_path)
            if import_status.is_ok():
                self.current_deck = import_status.value
            else:
                self.status_bar.show_timed_message(import_status.status)

        self.summary_model = SummaryCardsModel(self.current_deck)
        self.summary_view = ListingCardsTableView(self, self.summary_model)
        self.ui.main_layout.replaceWidget(self.ui.cards_table_view_placeholder, self.summary_view)
        self.ui.cards_table_view_placeholder.setParent(None)
        self.ui.cards_table_view_placeholder.deleteLater()

        self.input_model = InputCardsModel(self.summary_model)
        self.input_view = InputCardsTableView(self, self.input_model)
        self.ui.main_layout.replaceWidget(self.ui.input_table_view_placeholder, self.input_view)
        self.ui.input_table_view_placeholder.setParent(None)
        self.ui.input_table_view_placeholder.deleteLater()
        self.input_view.horizontalHeader().sectionResized.connect(self.update_tables_geometry)

        self.ui.menu_toggle_sidebar.setIcon(SharedIcons.Sidebar)
        self.ui.tbutton_toggle_sidebar.setDefaultAction(self.ui.menu_toggle_sidebar)
        self.ui.menu_toggle_sidebar.triggered.connect(self.action_toggle_sidebar)

        self.ui.menu_new.triggered.connect(self.action_new_deck)
        self.ui.menu_open.triggered.connect(self.action_open_project)
        self.ui.menu_save.triggered.connect(self.action_save_project)
        self.ui.menu_save_as.triggered.connect(self.action_save_project_as)
        self.ui.menu_export.triggered.connect(self.action_export_deck)

        self.show()
        self.restore_window_geometry()
        self.update_deck_metadata()

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

        is_sidebar_visible = Settings.get(StoredSettings.SIDEBAR_VISIBLE)
        self.ui.right_sidebar.setVisible(is_sidebar_visible)
        self.ui.menu_toggle_sidebar.setChecked(is_sidebar_visible)

        self.input_view.restore_geometry()
        self.update_tables_geometry()

    def store_window_geometry(self):
        self.input_view.store_geometry()
        Settings.set(StoredSettings.MAIN_WINDOW_GEOMETRY, self.geometry())
        Settings.set(StoredSettings.SIDEBAR_VISIBLE, self.ui.right_sidebar.isVisible())

    @Slot()
    def update_tables_geometry(self) -> None:
        new_header_sizes = self.input_view.header_sizes()
        self.summary_view.set_header_sizes(new_header_sizes)

    @Slot(ShortcutCommand)
    def on_shortcut_activated(self, shortcut_command: ShortcutCommand):
        if shortcut_command == ShortcutCommand.SUGGEST:
            self.lookup_and_suggest()
        # self.table_view.execute_shortcut_action(shortcut_command)

    @Slot()
    def action_toggle_sidebar(self):
        self.ui.right_sidebar.setVisible(not self.ui.right_sidebar.isVisible())
        self.ui.menu_toggle_sidebar.setChecked(self.ui.right_sidebar.isVisible())

    @Slot()
    def action_new_deck(self):
        # TODO: Save prompt
        self.current_deck = Deck('New Deck', [])
        self.update_deck_metadata()

    @Slot()
    def action_open_project(self):
        status_or = FileOperationsHelper.open_deck_select(self)
        if status_or.is_ok():
            self.current_deck = status_or.value
            self.update_deck_metadata()
        else:
            self.status_bar.show_timed_message(status_or.status)

    @Slot()
    def action_save_project(self):
        status = FileOperationsHelper.save_deck(self, self.current_deck)
        if not status.is_ok():
            self.status_bar.show_timed_message(status.status)

    @Slot()
    def action_save_project_as(self):
        status = FileOperationsHelper.save_deck_select(self, self.current_deck)
        if not status.is_ok():
            self.status_bar.show_timed_message(status.status)

    @Slot()
    def action_export_deck(self):
        status = FileOperationsHelper.export_deck_select(self, self.current_deck)
        if not status.is_ok():
            self.status_bar.show_timed_message(status.status)

    @Slot()
    def update_deck_metadata(self):
        self.ui.deck_info.setText('{} cards, {}'.format(
            len(self.current_deck.cards),
            self.current_deck.file_path.as_str() if self.current_deck.file_path is not None else 'brand new deck'
        ))

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
