from PySide6.QtCore import Signal, Slot, QSize, QPoint, QRect, Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QMainWindow, QApplication

from core.info import PROJECT_FULL_NAME
from core.settings import Settings, StoredSettings
from core.types import Deck
from ui.gen.main_window.main_window_uic import Ui_MainWindow
from ui.icons.list import IconsList
from ui.main_window.card_tables.input import InputCardsTableModel, InputCardsTableView
from ui.main_window.card_tables.overview import OverviewCardsTableModel, OverviewCardsTableView
from ui.main_window.status_bar import StatusBar


# Contains all lower-level UI operations handling and initializes child widgets.
# Application-level logic and operations with application data separated in Application and controller classes.
class MainWindow(QMainWindow):
    application_exit_requested = Signal()

    def closeEvent(self, event: QCloseEvent) -> None:
        # Signal Application class that exit was requested. If successful, it will set |application_closing| flag and
        # initiate window closing again.
        if self.application_closing:
            super().closeEvent(event)
            return
        event.ignore()
        self._store_geometry()
        self.application_exit_requested.emit()

    # Please note:
    # Non-top menu shortcuts are handled in shortcuts_controller.py
    # All file-related UI operations are handled in file_controller.py
    # All deck-related UI operations are handled in deck_controller.py
    def __init__(self, startup_deck: Deck):
        super().__init__()

        # Can be set by Application to indicate that all checks before closing were done.
        self.application_closing = False

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(PROJECT_FULL_NAME)

        self.status_bar: StatusBar = StatusBar(self)
        self.setStatusBar(self.status_bar)

        self.overview_model = OverviewCardsTableModel(startup_deck)
        self.overview_table_view = OverviewCardsTableView(self, self.overview_model)
        self.overview_table_view.setSizePolicy(self.ui.cards_table_overview_placeholder.sizePolicy())
        self.ui.main_layout.replaceWidget(self.ui.cards_table_overview_placeholder, self.overview_table_view)
        self.ui.cards_table_overview_placeholder.setParent(None)
        self.ui.cards_table_overview_placeholder.deleteLater()
        self.overview_table_view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        self.input_model = InputCardsTableModel()
        self.input_table_view = InputCardsTableView(self, self.input_model)
        self.input_table_view.setSizePolicy(self.ui.cards_table_input_placeholder.sizePolicy())
        self.ui.main_layout.replaceWidget(self.ui.cards_table_input_placeholder, self.input_table_view)
        self.ui.cards_table_input_placeholder.setParent(None)
        self.ui.cards_table_input_placeholder.deleteLater()
        self.input_table_view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        self.input_table_view.horizontalHeader().sectionResized.connect(self.sync_input_geometry_to_overview)
        self.input_table_view.horizontalScrollBar().valueChanged.connect(self.sync_input_geometry_to_overview)
        self.overview_table_view.horizontalScrollBar().valueChanged.connect(self.sync_overview_geometry_to_input)

        self.ui.top_menu_file_new.setIcon(IconsList.New)
        self.ui.top_menu_file_save.setIcon(IconsList.Save)
        self.ui.top_menu_file_open.setIcon(IconsList.Open)
        self.ui.top_menu_file_export.setIcon(IconsList.Export)
        self.ui.deck_info_save_button.setDefaultAction(self.ui.top_menu_file_save)

        self.ui.deck_info_toggle_sidebar_button.setDefaultAction(self.ui.top_menu_tools_toggle_sidebar)
        self.ui.top_menu_tools_toggle_sidebar.setIcon(IconsList.Sidebar)
        self.ui.top_menu_tools_toggle_sidebar.setChecked(Settings.get(StoredSettings.MAIN_WINDOW_SIDEBAR_VISIBLE))
        self.on_sidebar_toggled(self.ui.top_menu_tools_toggle_sidebar.isChecked())
        self.ui.top_menu_tools_toggle_sidebar.toggled.connect(self.on_sidebar_toggled)

        self.show()
        self._restore_geometry()

    def _restore_geometry(self):
        window_geometry: QRect = Settings.get(StoredSettings.MAIN_WINDOW_GEOMETRY)

        # At least 100px x 100px top-left part of the window is visible on one of the screens.
        def top_left_corner_visible(screen_rect: QRect):
            return screen_rect.contains(window_geometry.topLeft()) and \
                screen_rect.contains(window_geometry.topLeft() + QPoint(100, 100))

        if any((top_left_corner_visible(screen.geometry()) for screen in QApplication.screens())):
            self.setGeometry(window_geometry)
        else:
            current_screen = self.screen().geometry()
            min_size: QSize = self.minimumSize()
            half_min_size: QPoint = QPoint(min_size.width() / 2, min_size.height() / 2)
            self.setGeometry(QRect(current_screen.center() - half_min_size, min_size))

        self.input_table_view.restore_headers_geometry()

    def _store_geometry(self):
        self.input_table_view.store_headers_geometry()
        Settings.set(StoredSettings.MAIN_WINDOW_GEOMETRY, self.geometry())

    @Slot(bool)
    def on_sidebar_toggled(self, new_state: bool):
        self.ui.sidebar_widget.setVisible(new_state)
        Settings.set(StoredSettings.MAIN_WINDOW_SIDEBAR_VISIBLE, new_state)

    @Slot()
    def sync_input_geometry_to_overview(self):
        self.overview_table_view.set_header_sizes(self.input_table_view.get_header_sizes())
        self.overview_table_view.horizontalScrollBar().setValue(self.input_table_view.horizontalScrollBar().value())

    @Slot()
    def sync_overview_geometry_to_input(self):
        self.overview_table_view.set_header_sizes(self.input_table_view.get_header_sizes())
        self.input_table_view.horizontalScrollBar().setValue(self.overview_table_view.horizontalScrollBar().value())
