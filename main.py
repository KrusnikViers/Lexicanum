import sys

from PySide2.QtGui import Qt
from PySide2.QtWidgets import QApplication

from app.data.storage.csv import CSVWrapper
from ui.main_window import MainWindow

# Global initialization
CSVWrapper.register_dialect()

# Qt App & Window initialization
app = QApplication(sys.argv)

main_window = MainWindow()

# Main event loop
sys.exit(app.exec_())
