import sys

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow

app = QApplication(sys.argv)
main_window = MainWindow()
sys.exit(app.exec())
