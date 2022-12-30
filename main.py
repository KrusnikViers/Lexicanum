import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from ui.main_window.main_window import MainWindow

app = QApplication(sys.argv)
app.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.Floor)
main_window = MainWindow()
sys.exit(app.exec())
