from PySide2.QtWidgets import QMessageBox, QWidget


class Alert:
    _main_widget = None

    @classmethod
    def set_main_widget(cls, widget: QWidget):
        cls._main_widget = widget

    @classmethod
    def warning(cls, title: str, message: str):
        return QMessageBox.warning(cls._main_widget, title, message)
