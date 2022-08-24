import sys

from PySide2.QtWidgets import QApplication

from ui.main_window import MainWindow

# Qt App & Window initialization
app = QApplication(sys.argv)

main_window = MainWindow()

# Main event loop
sys.exit(app.exec_())
