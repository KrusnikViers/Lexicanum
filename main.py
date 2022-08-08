import sys

from PySide2.QtGui import Qt
from PySide2.QtWidgets import QApplication

from ui.main_window import MainWindow

app = QApplication(sys.argv)
app.setAttribute(Qt.AA_DisableWindowContextHelpButton)

main_window = MainWindow()
main_window.show()

sys.exit(app.exec_())
