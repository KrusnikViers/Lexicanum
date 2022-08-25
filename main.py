import sys

from PySide2.QtWidgets import QApplication

from ui.alert import Alert
from ui.main_window import MainWindow

# Qt App & Window initialization
app = QApplication(sys.argv)

main_window = MainWindow()
Alert.set_main_widget(main_window)

# Main event loop
sys.exit(app.exec_())
