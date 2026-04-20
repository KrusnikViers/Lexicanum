from PySide6.QtCore import Signal, SignalInstance, QSize, QPoint, QRect, Slot
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QMainWindow, QApplication

from anki import connection
from anki import wrapper
from base import info
from base import settings
from ui.main_window import main_window_uic
from ui.main_window import status_bar


# Use only for lower-level UI operations and setting child widgets.
# Complex logic should be moved to controller components.
class MainWindow(QMainWindow):
    exit_requested: SignalInstance = Signal()

    def closeEvent(self, event: QCloseEvent) -> None:
        # Signal Application class that exit was requested. If successful, it will close the window itself.
        event.ignore()
        self._store_geometry()
        self.exit_requested.emit()

    def __init__(self, *, anki_wrapper: wrapper.AnkiWrapper):
        super().__init__()

        self.ui = main_window_uic.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.button_disconnect_apply.clicked.connect(self._apply_settings_from_disconnect_screen)
        self.setWindowTitle(info.PROJECT_NAME_VERSION)

        self.status_bar = status_bar.StatusBar(self, info.VERSION_FULL)
        self.setStatusBar(self.status_bar)

        self._anki_wrapper = anki_wrapper
        self._anki_wrapper.connection.status_change.connect(self._on_updated_connection_status)

        self.show()
        self._restore_geometry()
        self._on_updated_connection_status(self._anki_wrapper.connection.status)

    @Slot()
    def _on_updated_connection_status(self, new_status: connection.ConnectionStatus):
        if new_status == connection.ConnectionStatus.CONNECTED:
            self.ui.stack_main.setCurrentWidget(self.ui.page_deck)
        else:
            self.ui.stack_main.setCurrentWidget(self.ui.page_disconnect)
            self.ui.edit_disconnect_url.setText(settings.ANKI_CONNECT_URL.get())
            self.ui.edit_disconnect_port.setValue(settings.ANKI_CONNECT_PORT.get())

    @Slot()
    def _apply_settings_from_disconnect_screen(self):
        settings.ANKI_CONNECT_URL.set(self.ui.edit_disconnect_url.text())
        settings.ANKI_CONNECT_PORT.set(self.ui.edit_disconnect_port.value())
        self._anki_wrapper.connection.maybe_refresh_connection()

    def _restore_geometry(self):
        stored_geometry: QRect = settings.UI_MAIN_WINDOW_GEOMETRY.get()
        self.setGeometry(stored_geometry)

        # Check that some area around top-left part of the window is visible on one of the screens.
        def top_left_corner_visible(screen_rect: QRect) -> bool:
            top_left = self.geometry().topLeft()
            return screen_rect.contains(top_left - QPoint(0, 10)) and screen_rect.contains(top_left + QPoint(50, 50))

        if not any((top_left_corner_visible(screen.geometry()) for screen in QApplication.screens())):
            current_screen = self.screen().geometry()
            min_size: QSize = self.minimumSize()
            half_min_size_point: QPoint = QPoint(min_size.width() // 2, min_size.height() // 2)
            self.setGeometry(QRect(current_screen.center() - half_min_size_point, min_size))

    def _store_geometry(self) -> None:
        settings.UI_MAIN_WINDOW_GEOMETRY.set(self.geometry())
